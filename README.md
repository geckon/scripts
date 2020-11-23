# scripts
Usually one purpose scripts provided without any warranty under the MIT
License. Read the disclaimer at the bottom of this readme.

[![Updates](https://pyup.io/repos/github/geckon/scripts/shield.svg)](https://pyup.io/repos/github/geckon/scripts/)

## Description

### Directly runnable

The following scripts are available in `bin` so you can include the directory
in your `$PATH` if you are brave or foolish enough:

##### `cr2_to_jpg.sh`
- Converts all CR2 RAW photos in the current directory to JPGs.
- Keeps the original files.
- Uses darktable (specifically `darktable-cli`).

##### `cut_video.sh`
- Copies a part (specified by time) of a video file to a new file.
- Uses `ffmpeg`.
- Run without arguments to print help.

##### `download_posts.py`
- Downloads forum posts specified by CSS classes. Can also include authors.
- Uses `requests` and `bs4` (see `download_posts/requirements.txt`).
- Run with `-h|--help` to print help.

##### `speedup_video.sh`
- Speeds up (or slows down) a video and stores it as a new file.
- Uses `ffmpeg`.
- Run without arguments to print help.

### Indirectly runnable

#### Image scraper

This is a very simple and stupid image scraper that will crawl a given website,
look for links to images and download them into specified path on your
filesystem. It can probably be used for scraping other files as well but it has
been written with images in mind.

There is a very important configuration inside `image_scraper/image_scraper.py`.
Double check that and the source code before running. Only then you may do:
```
$ pip install -r image_scraper/requirements.txt
$ scrapy runspider image_scraper/image_scraper.py
```

DO NOT run if you don't know what you're doing. It has been written and tested
with one particular website in mind and may very well not work for different
websites and/or screw something up.

## ☠ DISCLAIMER ☠
While there is no malicious code included on purpose and the scripts were
written with the best intentions, they may still do harm. Do not run any of
the scripts unless you examined and understood what they do and even then be
careful with them. The scripts may delete your files, destroy your computer,
blow your house up, injure people and even kill some kittens.
