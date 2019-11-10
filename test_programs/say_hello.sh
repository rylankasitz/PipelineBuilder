#!/bin/bash
#SBATCH--time=1:00

while [ "$1" != "" ]; do
	case $1 in
		--to_who) shift
					to_who=$1
					;;
		--output) shift
					output=$1
					;;
	esac
	shift
done

echo Hello $to_who > $output
