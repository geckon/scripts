#!/usr/bin/env python3

import argparse

import requests
from bs4 import BeautifulSoup

def parse_args():
    "Parse script's arguments."
    parser = argparse.ArgumentParser()
    parser.add_argument('url',
                        help='URL to be downloaded from')
    parser.add_argument('-p', '--post-class',
                        help='CSS class of posts',
                        required=True)
    parser.add_argument('-u', '--user-class',
                        help='add author to the result, expects CSS class')
    return parser.parse_args()

def include_div(css_class):
    if args.post_class == css_class:
        return True
    if args.user_class and args.user_class == css_class:
        return True
    return False

if __name__ == '__main__':
    args = parse_args()

    source = BeautifulSoup(requests.get(args.url).text, 'html.parser')
    result = ''

    for tag in source.find_all(class_=include_div):
        result += str(tag)

    print(BeautifulSoup(result, 'html.parser').prettify())

