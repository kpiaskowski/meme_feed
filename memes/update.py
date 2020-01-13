import argparse
import os
import time

import django
from facebook_scraper import get_posts
import logging

import config
from manage import DEFAULT_SETTINGS_MODULE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)
django.setup()
from memes.models import Meme


def update_memes(fanpages: list, num_pages: int):
    """
    Looks at FB fanpages and possibly adds new memes.
    :param fanpages: List of fanpages.
    :param num_pages: Number of pages of single fanpage to look.
    """
    count = 0
    new_count = 0
    try:
        memes = Meme.objects.all()
        for fanpage in fanpages:
            for post in get_posts(fanpage, pages=num_pages):
                count += 1
                post_url = post['post_url']
                post_id = post['post_id']
                image_url = post['image']

                if post_url and post_id and image_url:
                    if not memes.filter(post_id=post_id).exists():
                        new_meme = Meme(
                            post_id=post_id,
                            post_url=post_url,
                            image_url=image_url,
                            views=0,
                            valid=True
                        )
                        new_count += 1
                        new_meme.save()
        logging.info(f'Looked at {count} posts, added {new_count} new memes')
    except Exception as e:
        logging.exception("Exception occurred")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        filename='update_logs.log',
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
    )

    parser = argparse.ArgumentParser(description='Updates memes.')
    parser.add_argument('--num_pages', type=int, default=config.pages_to_search,
                        help='Num pages in single fanpage to look search')
    parser.add_argument('--fanpages', nargs='+', default=config.fanpages,
                        help='Fanpages to visit, usage: --fanpages convolutionalmemes artificial memes')
    parser.add_argument('--continuous_run', dest='continuous_run', action='store_true', default=True,
                        help="Run continuously, update memes every hour")
    parser.add_argument('--single_run', dest='continuous_run', action='store_false',
                        help="Run single update")
    parser.add_argument('--update_interval', default=config.update_interval,
                        help="Run single update")
    args = parser.parse_args()

    if args.continuous_run:
        # could be asynchronous but meh
        while True:
            update_memes(fanpages=args.fanpages, num_pages=args.num_pages)
            time.sleep(args.update_interval)  # run every 12h

    else:
        update_memes(fanpages=args.fanpages, num_pages=args.num_pages)
