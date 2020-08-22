# scripts
Usually one purpose scripts provided without any warranty under the MIT License.

[![Updates](https://pyup.io/repos/github/geckon/scripts/shield.svg)](https://pyup.io/repos/github/geckon/scripts/)

## Description

The following scripts are available in `bin` so you can include the directory in your `$PATH` if you are brave or foolish enough:

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

## DISCLAIMER
While there is no malicious code included on purpose and the scripts were written with the best intentions, they may still do harm. Do not run any of the scripts unless you examined and understood what they do and even then be careful with them. The scripts may delete your files, destroy your computer, blow your house up, injure people and even kill some kittens.
