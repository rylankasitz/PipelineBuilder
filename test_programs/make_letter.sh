#!/bin/bash
#SBATCH--time=1:00

while [ "$1" != "" ]; do
	case $1 in
		--greeting_file) shift
					greeting_file=$1
					;;
		--output) shift
					output=$1
					;;
	esac
	shift
done

cat $greeting_file > $output
echo How are you doing today? >> $output
