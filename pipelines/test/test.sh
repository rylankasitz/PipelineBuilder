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
		--count)
			shift
			count=$1
		;;
	esac
	shift
done

step=0
uuid="init"
mkdir -p $workspace/.steps
touch $workspace/.steps/$uuid.done

while [ $steps -lt "4" ]; do
	file=$workspace/.steps/$uuid.done
	if [ -f $file ]; then
		rm $workspace/.steps/$uuid.done
		if [ $step = "0" ]; then
			SBATCH D:\Rylan\Documents\Work\PipelineBuilder\programs/run_say_hello.sh --done $workspace/.steps/$uuid.done --to_who input --output $workspace/say_hello.txt
		fi
		if [ $step = "0" ]; then
			SBATCH D:\Rylan\Documents\Work\PipelineBuilder\programs/run_make_letter.sh --done $workspace/.steps/$uuid.done --greeting count 
		fi
		if [ $step = "0" ]; then
			counter=0

			for __entry__ in say_hello.txt/*.txt
			do
				SBATCH D:\Rylan\Documents\Work\PipelineBuilder\pipelines\test/inner_pipeline.sh --__Entry__ __Entry__ --workspace workspace/inner_pipeline_$count 
				let "counter++"
			done

			while [ $(ls -lR $say_hello.txt/../*.done | wc -l) -lt $counter ]; do
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