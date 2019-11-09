#!/bin/bash
#SBATCH--time=1:00

while [ "$1" != "" ]; do
	case $1 in
		--input) shift
					input=$1
					;;
		--count) shift
					count=$1
					;;
		--output) shift
					output=$1
					;;
	esac
	shift
done

cat input >> output
echo $count >> output