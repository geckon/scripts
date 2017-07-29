#! /bin/bash
#
# Simple video accelerator
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

COMMAND="ffmpeg"
SCRIPT=`basename "$0"`

########################################################################
# USAGE
########################################################################

USAGE="Simple video accelerator - usage:
\n\n
$SCRIPT source_file acceleration [dest_file]
\n\n
dest_file is not required - if it's missing, the result will be named as
the source_file with a suffix ("_ACCx" where ACC is acceleration) added
before the file extension.
\n\n
source_file won't be modified.
\n\n
acceleration can be less than 1 which will slow the video down
\n\n
EXAMPLES:
\n\n
$SCRIPT vids/myvideo.mp4 2 res/cut.mp4 \n
\t- speed up the video twice and store the result as res/cut.mp4
\n\n
$SCRIPT vids/myvideo2.mp4 0.5 \n
\t- speed up the video 0.5 times (i.e. make it twice as slow) and store
    it as myvideo2_0.5x.mp4 in the current directory
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
if [[ "$#" -lt 2 ]] || [[ "$#" -gt 3 ]] ; then
	echo -e $USAGE
	exit 0
fi

# Check the acceleration coefficient and its inversion
if [[ "$2" =~ ^[0-9]*\.?[0-9]+$ ]] ; then
	ACC=$2
else
	exit_err "ERROR: '$2' is not a valid acceleration coefficient." 3
fi
INV=`bc -l <<< "1 / $ACC"`

# Check that the important $COMMAND is installed
if ! type $COMMAND >/dev/null 2>&1 ; then
	exit_err "ERROR: You need $COMMAND installed to run this." 1
fi

# Determine dest_file
SUFFIX="_${ACC}x"
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

echo -e "Running\n $COMMAND -i $1 -filter_complex \"[0:v]setpts=$INV*PTS[v];[0:a]atempo=$ACC[a]\" -map \"[v]\" -map \"[a]\" -c:v libx264 -c:a aac $DEST"
$COMMAND -i $1 -filter_complex "[0:v]setpts=$ACC*PTS[v];[0:a]atempo=$INV[a]" -map "[v]" -map "[a]" -c:v libx264 -c:a aac $DEST

