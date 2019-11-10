#!/bin/bash

while [ "$1" != "" ]; do
	case $1 in
		--directoryname) shift
					directoryname=$1
					;;
		--$__loop__) shift
					$__loop__=$1
					;;
	esac
	shift
done

step=0
uuid="init"
touch $directoryname/../$uuid.done

while [ "$step" -lt "4" ]; do
	file=$directoryname/../$uuid.done
		if [ -f "$file" ]
		then
			sbatch progs/run_add_count.sh --input $__loop__ --count 100 --output $directoryname/../add_count.txt
			uuid=program1
		fi
		if [ -f "$file" ]
		then
			sbatch progs/run_add_count.sh --count 50 --input $directoryname/../add_count.txt 
			uuid=program2
		fi
	sleep 5
done
touch $directoryname/../<pipeline_uuid>.done