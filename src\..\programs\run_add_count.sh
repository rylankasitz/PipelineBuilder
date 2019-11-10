#!/bin/bash
#SBATCH--time=1:00

export PATH=":$PATH"

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

sbatch /homes/rylankasitz/PipelineBuilder/test_programs/repeat.sh --input $input --count $count --output $output

touch $done