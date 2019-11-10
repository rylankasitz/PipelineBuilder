#!/bin/bash
#SBATCH--time=1:00

export PATH="/../test_programs/:$PATH"

while [ "$1" != "" ]; do
	case $1 in
		--done) shift
					done=$1
					;;
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

sbatch $repeat --input $input --count $count --output $output

touch $done