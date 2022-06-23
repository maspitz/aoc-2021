#!/bin/sh

# Given a number NN,
# creates the NN/ directory, and
# creates the NN/dayNN.py and NN/test_NN.py files from templates.

if [ $# -ne 1 ]
then
	echo "Usage: $0 DAY_NUMBER "
	exit 1
fi

DAYNUM=`printf "%02d" $1`

if [ $DAYNUM -lt 1 -o $DAYNUM -gt 25 ]
then
	echo "$0: DAY_NUMBER must be between 1 and 25 inclusive "
	exit 1
fi

set -o noclobber

mkdir $DAYNUM

SEDCMD="s/DAY_NUMBER/${DAYNUM}/g"

sed -e $SEDCMD templates/dayNN.py > "${DAYNUM}/day${DAYNUM}.py"

# Avoid spurious octal literal by eliminating leading zero (if any).
sed -i -e "s/, day=0/, day=/" "${DAYNUM}/day${DAYNUM}.py"

sed -e $SEDCMD templates/_test_NN.py > "${DAYNUM}/test_${DAYNUM}.py"

