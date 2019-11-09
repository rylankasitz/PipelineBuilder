#!/bin/bash
#SBATCH--time=1-00:00:00

while [ "$1" != "" ]; do
	case $1 in
		one)		shift
					one=$1
					;;
		two)		shift
					two=$1
					;;
		three)		shift
					three=$1
					;;
	esac
	shift
done

python test.py $one -t $two > $three
