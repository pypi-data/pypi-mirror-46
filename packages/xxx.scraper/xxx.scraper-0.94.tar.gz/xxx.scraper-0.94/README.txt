1)
algoritm - scrap all posts inline

2)
bin/scraper_worker

3) go to 3 folder

from imagehash import dhash
from iso8601 import parse_date
from PIL import Image as PIL_Image

cur_im1 = PIL_Image.open('/home/t/Desktop/videos/3/test.jpg')
cur_hash1 = str(dhash(cur_im1))

GO TO REDIS select 1
set 2f2b0b2b33232323 "380668111208"


4)
import os
import redis
path = '/home/t/Desktop/videos/images'
two_dir = os.listdir(path)
r = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True, db=0)
keys = r.keys('*')
redis_values_dict = dict()
for key in keys:
    redis_values_dict[r.get(key)] = None
count = 0
for image in two_dir:
    if image not in redis_values_dict:
    os.remove('{}{}{}'.format(path, '/', image ))
    count += 1
