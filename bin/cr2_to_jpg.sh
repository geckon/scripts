#! /bin/bash
#
# Very simple CR2 to JPG converter
#
# Copyright (c) 2020 Tomáš Heger
# Available under the MIT License
#

for img in *.CR2
do
    echo "Converting $img"
    darktable-cli "$img" "$(basename ${img%.CR2}.jpg)";
done
