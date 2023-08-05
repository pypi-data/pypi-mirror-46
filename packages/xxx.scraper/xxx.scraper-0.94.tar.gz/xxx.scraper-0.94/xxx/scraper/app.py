from gevent import monkey
monkey.patch_all()

import argparse
import logging
import logging.config
import os
import sys
import yaml

from gevent import killall, sleep

from xxx.scraper.greenlets import WatcherGreenlet, PutUrlsQueueGreenlet, PostGreenlet

logger = logging.getLogger('Bridge')


def main():
    parser = argparse.ArgumentParser(description='---- App ----')
    parser.add_argument('app_config', type=str,
                        help='App Configuration File')

    args = parser.parse_args()
    if os.path.isfile(args.app_config):
        app_defaults = yaml.load(open(args.app_config))
        logging.config.dictConfig(app_defaults)
    else:
        logger.info('App defaults config doesnot exist!')
        print("App defaults config doesnot exist!")
        sys.exit(1)

    try:
        w1 = PutUrlsQueueGreenlet.spawn(app_defaults)
        w2 = PostGreenlet.spawn(app_defaults)
        w3 = WatcherGreenlet.spawn(
            app_defaults, w1, w2
        )
        while True:
            sleep(1000)
    except (KeyboardInterrupt, SystemExit):
        logger.info('Killing all')
        killall([w3, w2, w1])


if __name__ == '__main__':
    main()
