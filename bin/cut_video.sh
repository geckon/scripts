#! /bin/bash
#
# Simple video cutter
#
# Copyright (c) 2017 Tomáš Heger
# Available under the MIT License
#
# For help run without arguments.
#

########################################################################
# INIT
########################################################################

# Exit if a command fails or a variable is unset
set -e
set -u

SUFFIX="_cut"
COMMAND="ffmpeg"

########################################################################
# USAGE
########################################################################

USAGE="Simple video cutter - usage:
\n\n
$0 source_file start length [dest_file]
\n\n
dest_file is not required - if it's missing, the result will be named as
the source_file with $SUFFIX added before the file extension.
\n\n
source_file won't be modified.
\n\n
EXAMPLES:
\n\n
$0 vids/myvideo.mp4 00:00:42 00:00:13 res/cut.mp4 \n
\t- cut 13 seconds from vids/myvideo.mp4 starting from the 42nd second
    and store the result as res/cut.mp4
\n\n
$0 vids/myvideo2.mp4 00:00:00 00:01:00 \n
\t- cut the first minute from vids/myvideo2.mp4 and store it as
    myvideo2_cut.mp4 in the current directory
\n"


########################################################################
# FUNCTIONS
########################################################################

# Print $1 to stderr and exit with $2
exit_err() {
	>&2 echo "$1"
	exit "$2"
}

########################################################################
# PROCESS ARGUMENTS
########################################################################

# If there is wrong number of arguments, print help
if [[ "$#" -lt 3 ]] || [[ "$#" -gt 4 ]] ; then
	echo -e $USAGE
	exit 0
fi

# Check that the important $COMMAND is installed
if ! type $COMMAND >/dev/null 2>&1 ; then
	exit_err "ERROR: You need $COMMAND installed to run this." 1
fi

# Determine dest_file
if [[ "$#" -eq 4 ]] ; then
	DEST="$4"
else
	FILE=`basename "$1"`
	NAME="${FILE%.*}"
	if [[ $FILE =~ \. ]] ; then
		EXT=".${FILE##*.}"
	else
		EXT=""
	fi
	DEST="$NAME$SUFFIX$EXT"
fi

# Check that dest_file doesn't already exist
if [[ -f $DEST ]] || [[ -d $DEST ]] ; then
	exit_err "ERROR: '$DEST' already exists. I won't overwrite it." 2
fi

########################################################################
# MAIN CODE
########################################################################

echo -e "Running\n $COMMAND -ss $2 -i $1 -t $3 -vcodec copy -acodec copy $DEST"
$COMMAND -ss $2 -i $1 -t $3 -vcodec copy -acodec copy $DEST

