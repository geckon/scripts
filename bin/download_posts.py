#!/usr/bin/env python3

import argparse
import sys

import requests
from bs4 import BeautifulSoup


def parse_args():
    "Parse script's arguments."
    parser = argparse.ArgumentParser(
        usage='Extract tags specified by CSS classes. Primarily '
              'intended to be used to download forum posts.')
    parser.add_argument('url',
                        help='URL to be downloaded from')
    parser.add_argument('-p', '--post-class',
                        help='CSS class of posts',
                        required=True)
    parser.add_argument('-u', '--user-class',
                        help='add author to the result, expects CSS class')
    parser.add_argument('-i', '--ignore-class',
                        action='append',
                        help='CSS class that should be ignored, can be '
                             'provided multiple times to ignore '
                             'multiple tag classes')
    parser.add_argument('-r', '--add-hr',
                        action='store_true',
                        help='Add <HR> tag after each tag added to the '
                             'result')
    parser.add_argument('-D', '--debug',
                        action='store_true',
                        help='Print debug messages (to stderr).')
    return parser.parse_args()


def debug_msg(msg):
    "Print the given message to stderr if debug mode is enabled."
    if args.debug:
        print("DEBUG: " + msg + "\n", file=sys.stderr)


def include_tag(css_class):
    """Should this tag be included in the result?

    Return True if the given css_class is either post_class or
    user_class provided by the user as a CLI argument, False otherwise.
    """
    if args.post_class == css_class:
        return True
    if args.user_class and args.user_class == css_class:
        return True
    return False


def ignore_tag(css_class):
    """Should this tag be ignored in the result?

    Return True if the given css_class is among ignore-class arguments
    provided by the user via CLI, False otherwise.
    """
    return css_class in args.ignore_class

if __name__ == '__main__':
    args = parse_args()

    # download the page
    response = requests.get(args.url)
    debug_msg("Downloaded '{}' with HTTP code {}".format(args.url,
                                                         response.status_code))
    source = BeautifulSoup(response.text, 'html.parser')
    debug_msg("The HTML source:\n{}".format(source))

    # collect the wanted tags
    result = ''
    for tag in source.find_all(class_=include_tag):
        result += str(tag)
        debug_msg("Adding tag:\n{}".format(tag))
        if args.add_hr:
            result += '<HR>'

    # remove the not wanted tags
    res_soup = BeautifulSoup(result, 'html.parser')
    for tag in res_soup(class_=ignore_tag):
        debug_msg("Removing tag:\n{}".format(tag))
        tag.extract()

    # print the result
    print(res_soup.prettify())
