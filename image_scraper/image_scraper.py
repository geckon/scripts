import hashlib
import os
import requests
import scrapy
import urllib


"""
This is a very simple and stupid image scraper that will crawl a given website
(INITIAL_URL), look for links to images (files ending with an extension
specified in IMAGE_EXTENSIONS) according to IMAGE_HREF_XPATH, depending on
BROWSE_SUBDIRECTORIES it will also look into "subdirectories" or not and store
all the images to a directory specified by PATH_TO_IMAGE_STORE (all image
filenames are updated with the image's checksum to avoid downloading the same
image twice if it's linked twice). It may or may not create subdirectory
structure based on CREATE_SUBDIRECTORIES.

See Config below.

Run:
$ scrapy runspider image_scraper.py

No guarantees at all provided. DO NOT run if you don't know what you're doing.
It has been written and tested with one particular website in mind and may very
well not work for different websites and/or screw something up.
"""


# Config:
#
# Add checksum to filename?
ADD_CHECKSUM_TO_FILENAME = False
#
# Collect ignored (non considered image) extensions? Does not affect the image
#  collecting itself.
COLLECT_IGNORED_EXTENSIONS = False
#
# Image extensions to download. It should also work for non-image file
#  extensions.
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
# Browse "subdirectories" or not? The logic is very stupid and it will consider
#  any path not containing a dot a directory.
BROWSE_SUBDIRECTORIES = True
#
# Recreate the directory structure and store images into subdirectories as
#  opposed to storing everything in one flat directory?
CREATE_SUBDIRECTORIES = True


def is_url_absolute(url):
    """Return True if the given url is absolute, False otherwise."""
    return bool(urllib.parse.urlparse(url).netloc)


def is_url_external(url):
    """Return True if the url is external comparing to INITIAL_URL."""
    return (
        is_url_absolute(url) and
        not url.startswith(INITIAL_URL)
    )

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
            # Skip external links.
            if is_url_external(href):
                continue

            href_split = href.rsplit('.')
            if not href_split:
                # Empty href?
                continue
            elif len(href_split) == 1:
                # This is probably a subdirectory.
                if not BROWSE_SUBDIRECTORIES:
                    continue

                # Prepare parameters for recursive runs.
                meta_params = {}
                if COLLECT_IGNORED_EXTENSIONS:
                    meta_params['ignored_exts'] = ignored_exts
                if CREATE_SUBDIRECTORIES:
                    meta_params['relative_path'] = os.path.join(
                        response.meta.get('relative_path', ''),
                        urllib.parse.unquote_plus(href)
                    )

                # Dive into it.
                yield scrapy.Request(
                    response.urljoin(href),
                    self.parse,
                    meta=meta_params
                )
            elif href_split[1] in IMAGE_EXTENSIONS:
                # Get the image.
                image_url = urllib.parse.urljoin(response.url, href)
                image_response = requests.get(image_url, stream=True)
                if not image_response.ok:
                    continue

                # Compute the checksum and filename.
                image_bytes = image_response.raw.read()
                # Make filename readable better, also use basename only.
                without_ext = urllib.parse.unquote_plus(
                    os.path.basename(href_split[0])
                )
                if ADD_CHECKSUM_TO_FILENAME:
                    image_hash = hashlib.md5(image_bytes).hexdigest()
                    filename = f'{without_ext}_{image_hash}.{href_split[1]}'
                else:
                    filename = f'{without_ext}.{href_split[1]}'


                # Determine filesystem path.
                if CREATE_SUBDIRECTORIES:
                    dir_path = os.path.join(
                        PATH_TO_IMAGE_STORE,
                        response.meta.get('relative_path', '')
                    )
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                else:
                    dir_path = PATH_TO_IMAGE_STORE
                filepath = os.path.join(dir_path, filename)

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
