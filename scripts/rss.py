import argparse
import hashlib
import re
import sys

import feedparser
import requests as req
from feedgen.feed import FeedGenerator
from retry import retry

BASE_ID = None
HASH_SALT = None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("data")
    return parser.parse_args()


def get_entry_attachment(e):
    pass


def convert_entry(e):
    link, title = get_entry_attachment(e)
    pass


def convert_feed(original):
    feed_attrs = {
        'title': None,
        'id': BASE_ID,
        'subtitle': (None, None),
        'author': {
            'name': None
        },
        'language': 'en',
        'link': {
            'href': (
                "https://github.com/data-liberation-project/",
                "phmsa-hazmat-incident-reports"
            )
        },
        'updated': original.feed.updated,
    }

    fg = FeedGenerator()
    for k, v in feed_attrs.items():
        getattr(fg, k)(v)

    for e in reversed(original.entries):
        new_entry = fg.add_entry()
        for k, v in convert_entry(e).items():
            method = getattr(new_entry, k)
            if isinstance(v, dict):
                method(**v)
            else:
                method(v)
    
    return fg


#TODO: Convert this to a feed that read the most recent data entries
@retry(tries=4, delay=15)
def fetch_feed(data_path):
    #TODO: create object getting most recent entries into files in data_path as a "feed"
    feed_content = None
    return feed_content


def main():
    args = parse_args()
    feed_content = fetch_feed(args.data)
    original = feedparser.parse(feed_content)
    converted = convert_feed(original)
    converted.rss_file(sys.stdout.buffer, pretty=True)


if __name__ == "__main__":
    main()
