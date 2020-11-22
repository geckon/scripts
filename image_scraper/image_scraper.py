import hashlib
import os
import requests
import scrapy
import urllib


"""
This is a very simple and stupid image scraper that will crawl a given website
(INITIAL_URL), look for images (files ending with an extension specified in
IMAGE_EXTENSIONS) according to IMAGE_HREF_XPATH, depending on SUBDIRECTORIES it
will also look into "subdirectories" or not and store all the images to
a directory specified by PATH_TO_IMAGE_STORE (all image filenames are updated
with the image's checksum to avoid downloading the same image twice if it's
linked twice).

See Config below.

Run:
$ scrapy runspider image_scraper.py

No guarantees at all provided. DO NOT run if you don't know what you're doing.
It may very well screw something up.
"""


# Config:
#
# Collect ignored (non considered image) extensions? Does not affect the image
#  collecting itself.
COLLECT_IGNORED_EXTENSIONS = False
#
# Image extensions to download.
IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png']
#
# Where to look for image URLs?
IMAGE_HREF_XPATH = '//td/a/@href'
#
# Where to start?
INITIAL_URL = ''
#
# Filesystem path to store images to.
PATH_TO_IMAGE_STORE = ''
#
# Browse "SUBdirectories" or not? The logic is very stupid and it will consider
#  any path not containing a dot a directory.
SUBDIRECTORIES = True


class ImageSpider(scrapy.Spider):
    name = 'image_spider'
    start_urls = [INITIAL_URL]

    def parse(self, response):
        if COLLECT_IGNORED_EXTENSIONS:
            # Use this set to collect all extensions that were found but were not
            #  considered image extensions. There is no other purpose to this
            #  variable and it can be removed without breaking the functionality.
            if response.meta.get('ignored_exts') is None:
                ignored_exts = set()
            else:
                ignored_exts = response.meta.get('ignored_exts')

        for href in response.xpath(IMAGE_HREF_XPATH).getall():
            href_split = href.rsplit('.')
            if not href_split:
                # Empty href?
                continue
            elif len(href_split) == 1:
                # This is a subdirectory.
                if not SUBDIRECTORIES:
                    continue

                # Dive into it.
                if COLLECT_IGNORED_EXTENSIONS:
                    yield scrapy.Request(
                        response.urljoin(href),
                        self.parse,
                        meta={'ignored_exts': ignored_exts}
                    )
                else:
                    yield scrapy.Request(response.urljoin(href), self.parse)
            elif href_split[1] in IMAGE_EXTENSIONS:
                # Get the image.
                image_url = urllib.parse.urljoin(response.url, href)
                response = requests.get(image_url, stream=True)
                if not response.ok:
                    continue

                # Compute the checksum and path.
                image_bytes = response.raw.read()
                image_hash = hashlib.md5(image_bytes).hexdigest()
                # Make filename readable better.
                without_ext = urllib.parse.unquote_plus(href_split[0])
                filename = f'{without_ext}_{image_hash}.{href_split[1]}'
                filepath = os.path.join(PATH_TO_IMAGE_STORE, filename)

                # Skip we already have this.
                if os.path.exists(filepath):
                    continue

                # Save the image.
                with open(filepath, 'wb') as out_file:
                    out_file.write(image_bytes)
            elif COLLECT_IGNORED_EXTENSIONS:
                ignored_exts.add(href_split[1])

        if COLLECT_IGNORED_EXTENSIONS:
            print(f'These extensions were also found but not used: {ignored_exts}')
