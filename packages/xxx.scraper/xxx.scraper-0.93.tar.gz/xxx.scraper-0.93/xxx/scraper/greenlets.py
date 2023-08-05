from gevent import monkey
monkey.patch_all()

import os
import logging
import re
import redis
import requests
import traceback

from bs4 import BeautifulSoup
from couchdb import Server as CouchdbServer
from datetime import datetime
from gevent import Greenlet, sleep
from gevent.queue import Queue
from imagehash import dhash
from iso8601 import parse_date
from random import choice
from requests.sessions import Session
from PIL import Image as PIL_Image

from xxx.server_api.models import Number, Post, Image
from xxx.scraper.utils import (
    agents,
    cities_dict,
    headers,
    max_posts_per_day,
    timeout,
)


logger = logging.getLogger('Bridge')
post_urls_queue = Queue()


class PutUrlsQueueGreenlet(Greenlet):

    def __init__(self, app_defaults):
        Greenlet.__init__(self)
        self.sleep_seconds = app_defaults['bridge_config']['puturlsqueue_greenlet']['sleep_seconds']
        server = CouchdbServer(app_defaults['bridge_config']['couchdb_server'])
        self.db = server[app_defaults['bridge_config']['couchdb_database']]
        # self.html = 'http://ukrgo.com/view_subsection.php?id_subsection=146'
        self.html = 'http://lvov.ukrgo.com/view_subsection.php?id_subsection=146'
        self.search = '&search=&page='

        logger.info('Started {}'.format(self))

    def get_posts_from_single_page(self, html_page, update=False):
        html = requests.get(html_page, timeout=timeout).__dict__['_content']
        soup = BeautifulSoup(html, 'html.parser')
        l = []
        for x in soup.find_all('a', {'class': 'link_post'}):
            l.append(x['href'])
        l = l[3:53:2]
        if update:
            if l and l[0] != self.last_scraped_post:
                self.last_scraped_post_doc['post'] = l[0]
                self.db.save(self.last_scraped_post_doc)
        return l

    def _run(self):
        # make as decorator , refactor later
        if 'last_scraped_post' not in self.db:
            self.db['last_scraped_post'] = {'post': ''}
        while True:
            self.last_scraped_post_doc = self.db.get('last_scraped_post')
            self.last_scraped_post = self.last_scraped_post_doc['post']

            for x in range(1, 20):
                html_page = '{}{}{}'.format(self.html, self.search, x)
                outer_break = False
                if x == 1:
                    posts = self.get_posts_from_single_page(html_page, update=True)
                else:
                    posts = self.get_posts_from_single_page(html_page)
                if not posts:
                    logger.info('No posts')
                    outer_break = True
                for post in posts:
                    if post != self.last_scraped_post:
                        logger.info('Put into queue {}'.format(post))
                        post_urls_queue.put(post)
                    else:
                        logger.info('Last scraped found breaking')
                        outer_break = True
                        break
                if outer_break:
                    break
            logger.info('Sleeping for {}'.format(self.sleep_seconds))
            sleep(self.sleep_seconds)

    def __str__(self):
        return 'PutUrlsQueueGreenlet({})'.format(self.sleep_seconds)


class WatcherGreenlet(Greenlet):
    def __init__(self, app_defaults, put_urls_queue_g, post_g):
        Greenlet.__init__(self)
        self.app_defaults = app_defaults
        self.interval_seconds = app_defaults['bridge_config']['watcher_greenlet']['sleep_seconds']
        self.put_urls_queue_g = put_urls_queue_g
        self.post_g = post_g

        logger.info('Started {}'.format(self))

    def _run(self):
        while True:
            if len(post_urls_queue) > 0:
                logger.info('Len of post_urls_queue is {}'.format(
                    len(post_urls_queue)
                ))
            if self.put_urls_queue_g.dead:
                logger.info('Put url greenlet is dead. Respawning')
                w1 = PutUrlsQueueGreenlet.spawn(
                    self.app_defaults['bridge_config']['puturlsqueue_greenlet']['sleep_seconds']
                )
                self.put_urls_queue_g = w1
            if self.post_g.dead:
                logger.info('Post greenlet is dead. Respawning')
                w2 = PostGreenlet.spawn(self.app_defaults)
                self.post_g = w2
            sleep(self.interval_seconds)

    def __str__(self):
        return 'WatcherGreenlet({})'.format(self.interval_seconds)


class PostGreenlet(Greenlet):
    age_regex = re.compile('.*?([0-9]{2}).год.*')
    city_regex = re.compile('^http://(\D+)\.ukrgo.+')
    height_regex = re.compile('.*?([0-9]{3}).см.*')
    number_regex = re.compile('(\d{10})')
    time_regex = re.compile('.*?([0-9]{1,2}.[0-9]{1,2}.[0-9]{4}.[0-9]{1,2}.[0-9]{1,2}).*')
    weight_regex = re.compile('.*?([0-9]{2,3}).кг.*')

    numbers_basket = dict()

    def __init__(self, app_defaults):
        Greenlet.__init__(self)
        self.sleep_seconds = app_defaults['bridge_config']['post_greenlet']['sleep_seconds']

        self.static_path = app_defaults['bridge_config']['post_greenlet']['static_path'] + 'temp_images/'
        self.static_path_done = app_defaults['bridge_config']['post_greenlet']['static_path'] + 'images/'

        server = CouchdbServer(app_defaults['bridge_config']['couchdb_server'])
        self.db = server[app_defaults['bridge_config']['couchdb_database']]

        redis_host = app_defaults['bridge_config']['post_greenlet']['redis']['host']
        redis_port = app_defaults['bridge_config']['post_greenlet']['redis']['port']

        redis_black_list_db = app_defaults['bridge_config']['post_greenlet']['redis']['db']['black_list']
        self.black_list_numbers = redis.StrictRedis(
            host=redis_host, port=redis_port, charset="utf-8", decode_responses=True, db=redis_black_list_db)
        redis_image_hash_db = app_defaults['bridge_config']['post_greenlet']['redis']['db']['image_hash']
        self.image_hashe = redis.StrictRedis(
            host=redis_host, port=redis_port, charset="utf-8", decode_responses=True, db=redis_image_hash_db)

        logger.info('Started {}'.format(self))

    def __str__(self):
        return 'PostGreenlet'

    def get_number_string(self, input_number):
        res = self.number_regex.match(input_number)
        if res and res.group(1):
            return '{}{}'.format('38', res.group(1))

    def get_number_from_couchdb(self, number_var):
        if number_var in self.numbers_basket:
            return self.numbers_basket[number_var]
        number = self.db.get(number_var)
        if number:
            number = Number(number)
            self.numbers_basket[number_var] = number
            return number
        else:
            number = Number()
            number._id = number_var
            self.numbers_basket[number_var] = number
            return number

    def get_post_from_soup(self, post_url, soup):
        post = Post()
        post.url_link = post_url

        match_city = re.match(self.city_regex, str(post_url))  # here add city
        if match_city:
            post.city = cities_dict[match_city.group(1)]

        title_h1s = soup.findAll("h1",
                                 {"style": "display: inline; font-size: 20px; font-weight: normal;"})
        try:
            post.title = title_h1s[0].contents[0].strip()
        except Exception as e:
            logger.error("No title for ", post_url)

        description_divs = soup.findAll("div", {
            "style": "margin-top: 15px; text-align: left; width: 100%; color: #2a2a2a; font-size: 14px;"})
        if description_divs:
            post.description = description_divs[0].contents[0].strip()[:2999]  # avoid max size for model
        else:
            logger.error('No description for ', post_url)

        # here add age weight height
        specific_div_info = soup.findAll("div", {"style": "color: #242424; font-size: 12px; margin-top: 5px;"})
        specific_str = str(specific_div_info[0])

        specific_splited = specific_str.split('\n')
        temp_str = ''.join(specific_splited)

        match_age = re.match(self.age_regex, temp_str)
        if match_age:
            post.age = int(match_age.group(1))
        match_weight = re.match(self.weight_regex, temp_str)
        if match_weight:
            post.weight = int(match_weight.group(1))
        match_height = re.match(self.height_regex, temp_str)
        if match_height:
            post.height = int(match_height.group(1))

        # here add time
        # should stich to iso 8601 "2018-06-30T00:00:00+03:00"
        match_time = re.match(self.time_regex, temp_str)
        if match_time:
            time_str = match_time.group(1)
            t_l = time_str.split('.')
            t_l[2] = t_l[2].split()
            t_l[2][1] = t_l[2][1].split(':')
            post.date_post = parse_date(
                '{}-{}-{}T{}:{}:00+02:00'.format(t_l[2][0], t_l[1], t_l[0], t_l[2][1][0], t_l[2][1][1]))
        else:
            post.date_post = datetime.now()

        # images actions here
        # http://odessa.ukrgo.com/pictures/ukrgo_id_19919685.jpg
        im_url_splited = post_url.split('/post')
        post_ims = soup.findAll("img", {"class": "image_galary"})
        for image_tag in post_ims:
            image = Image()
            image.source = im_url_splited[0] + image_tag.attrs['src'][1:]
            post.images.append(image)

        return post

    def process_post_images(self, post):
        for image in post.images:
            add_image = True
            try:
                response = requests.get(image.source, timeout=timeout)
            except Exception as e:
                image.link = None
                logger.error(e)
                logger.error('Connection error utils 272')
                continue
            try:
                if response.status_code == 200:
                    url_array = image.source.split('/')
                    temp_new_image_path = '{}{}'.format(self.static_path, url_array[-1])
                    with open(temp_new_image_path, 'wb') as destination_file:
                        destination_file.write(response.__dict__['_content'])
                else:
                    image.link = None
                    continue

                cur_im = PIL_Image.open(temp_new_image_path)
                cur_hash = str(dhash(cur_im))
                redis_item_url = self.image_hashe.get(cur_hash)
                if redis_item_url:
                    image.link = redis_item_url
                    add_image = False
                else:
                    self.image_hashe.set(cur_hash, url_array[-1])

                if add_image:
                    # here move one file to other destination
                    os.rename(temp_new_image_path, self.static_path_done + url_array[-1])
                    image.link = url_array[-1]
                else:
                    os.remove(temp_new_image_path)
            except Exception as e:
                logger.critical(e)
                logger.error('greenlets 231')

    def _run(self):
        try:
            while True:
                if not len(post_urls_queue):
                    logger.info('Post queue is empty sleepping {}'.format(self))
                    sleep(self.sleep_seconds)
                    continue
                post_url = post_urls_queue.get()
                session = Session()
                current_headers = headers.update({'User-Agent': choice(agents)})

                response = session.get(post_url, headers=current_headers, timeout=timeout)

                soup = BeautifulSoup(response.content, 'html.parser')
                credentials = soup.find_all(attrs={'class': 'post-contacts'})
                if not credentials:
                    logger.error('No credentials, skipping, url={}'.format(post_url))
                    continue
                inps = credentials[0].find_all('input')
                showPhonesWithDigits_text = inps[0]['onclick']
                indexes = [m.start() for m in re.finditer("'", showPhonesWithDigits_text)]

                data = {'i': showPhonesWithDigits_text[indexes[0]+1: indexes[1]],
                        's': showPhonesWithDigits_text[indexes[2]+1: indexes[3]]}
                #update headers
                current_headers = {}.update({
                    'Accept': 'text/html, */*; q=0.01',
                    'Cookie': 'ukr_go={}; b=b'.format(session.cookies.get('ukr_go')),
                    'Content-Length': '53',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Host': 'lvov.ukrgo.com',
                    'Referer': post_url.encode('utf-8'),
                    'X-Requested-With': 'XMLHttpRequest'
                })
                response_credentials = session.post('http://lvov.ukrgo.com/moduls/showphonesnumbers.php',
                                        data=data, headers=current_headers, timeout=timeout)

                number_soup = BeautifulSoup(response_credentials.content, 'html.parser')
                if not number_soup.span:
                    logger.error('No span, skipping, url={}'.format(post_url))
                    continue
                number = self.get_number_string(number_soup.span.text)
                if not number:
                    logger.error('No number, skipping, url={}'.format(post_url))
                    continue
                if self.black_list_numbers.get(number):
                    logger.info('Got blacklisted, skipping {}'.format(number))
                    sleep(1)
                    continue
                number = self.get_number_from_couchdb(number)
                post = self.get_post_from_soup(post_url, soup)

                if post in number.posts:
                    logger.info('Post already exist, skipping {}'.format(number))
                    continue
                elif number.posts and \
                        len([p for p in number.posts[-1: -30: -1] if
                             p.date_post.date() == post.date_post.date()]) >= max_posts_per_day:
                    logger.info('Max posts per day limit, skipping {}'.format(number))
                    continue
                else:
                    images_count = len({im.link for post in number.posts for im in post.images})
                    if images_count < 11:
                        self.process_post_images(post)
                    number.posts.append(post)
                    number.last_post_date = post.date_post
                    number.store(self.db)
                    # filter only for cities
                    if len({p.city for p in number.posts}) > 3:
                        self.black_list_numbers.set(number._id, True)
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(e)
            logger.error('Error 353')
