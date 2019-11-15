#!/bin/bash

while [ $1 != "" ]; do
	case $1 in
		--workspace)
			shift
			workspace=$1
		;;
		--input)
			shift
			input=$1
		;;
	esac
	shift
done

step=0
uuid="init"
mkdir -p $workspace/.steps
touch $workspace/.steps/$uuid.done

while [ $steps -lt "2" ]; do
	file=$workspace/.steps/$uuid.done
	if [ -f $file ]; then
		rm $workspace/.steps/$uuid.done
		if [ $step = "0" ]; then
			counter=0

			for __entry__ in input/*_greet.txt
			do
				SBATCH D:\Rylan\Documents\Work\PipelineBuilder\pipelines\greetings/edit_greetings.sh --__entry__ __entry__ --workspace workspace/edit_greetings_$count 
				let "counter++"
			done

			while [ $(ls -lR $input/../*.done | wc -l) -lt $counter ]; do
				sleep 30
			done

			touch workspace/.steps/uuid.done
			rm --rf workspace/.steps/uuid.done
			uuid="loop"
		fi
		let "step++"
	fi
	sleep 30
done