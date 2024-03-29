#!/bin/bash

while [ $1 != "" ]; do
	case $1 in
		--workspace)
			shift
			workspace=$1
		;;
		--__entry__)
			shift
			__entry__=$1
		;;
	esac
	shift
done

step=0
uuid="init"
mkdir -p $workspace/.steps
touch $workspace/.steps/$uuid.done

while [ $steps -lt "3" ]; do
	file=$workspace/.steps/$uuid.done
	if [ -f $file ]; then
		rm $workspace/.steps/$uuid.done
		if [ $step = "0" ]; then
			SBATCH D:\Rylan\Documents\Work\PipelineBuilder\programs/run_say_hello.sh --done $workspace/.steps/$uuid.done --to_who __entry__ --output $workspace/say_hello.txt
		fi
		if [ $step = "0" ]; then
			SBATCH D:\Rylan\Documents\Work\PipelineBuilder\programs/run_make_letter.sh --done $workspace/.steps/$uuid.done --greeting say_hello.txt --output $workspace/make_letter.txt
		fi
		let "step++"
	fi
	sleep 30
done