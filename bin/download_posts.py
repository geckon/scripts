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
                        help='URL to be downloaded from',
                        nargs='?')
    parser.add_argument('-f', '--file',
                        help='file to filter; needed if no URL is provided')
    parser.add_argument('-e', '--encoding',
                        help='file encoding; used only with -f|--file option')
    parser.add_argument('-a', '--add-class',
                        action='append',
                        required=True,
                        help='CSS class that should be added to the result, '
                             'can be provided multiple times to add multiple '
                             'tag classes')
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
    parser.add_argument('-l', '--recursion-limit',
                        type=int,
                        help='Overwrite recursion limit (may be needed for '
                             'large threads; use with caution)')
    args = parser.parse_args()

    if (not args.url and not args.file) or (args.url and args.file):
        print('ERROR: URL or file need to be provided but not both.',
              file=sys.stderr)
        exit(1)

    if args.recursion_limit:
        sys.setrecursionlimit(args.recursion_limit)

    return args


def debug_msg(msg):
    "Print the given message to stderr if debug mode is enabled."
    if args.debug:
        print("DEBUG: " + msg + "\n", file=sys.stderr)


def include_tag(css_class):
    """Should this tag be included in the result?

    Return True if the given css_class is either post_class or
    user_class provided by the user as a CLI argument, False otherwise.
    """
    return css_class in args.add_class


def ignore_tag(css_class):
    """Should this tag be ignored in the result?

    Return True if the given css_class is among ignore-class arguments
    provided by the user via CLI, False otherwise.
    """
    return css_class in args.ignore_class


if __name__ == '__main__':
    args = parse_args()

    if args.url:
        # download the page
        response = requests.get(args.url)
        debug_msg("Downloaded '{}' with HTTP code {}".format(
            args.url, response.status_code))
        source = BeautifulSoup(response.text, 'html.parser')
    else:
        # read the file
        debug_msg("Reading file '{}'".format(args.file))
        if args.encoding:
            f = open(args.file, 'r', encoding=args.encoding)
        else:
            f = open(args.file, 'r')
        source = BeautifulSoup(f.read(), 'html.parser')
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
