#!/bin/bash

export PATH="$(realpath "/pipelines/big_boi"):$PATH"

while [ "$1" != "" ]; do
	case $1 in
		--directoryname) shift
					directoryname=$1
					;;
		--input) shift
					input=$1
					;;
	esac
	shift
done

step=0
uuid="init"
touch $directoryname/$uuid.done

while [ "$step" -lt "1" ]; do
	file=$directoryname/$uuid.done
		if [ -f "$file" ]
		then
			loopname=$input
			file_counter=0

			for entry in $loopname/*.txt
			do
				mkdir -p $loopname/../the_pipeline/$file_counter
				sbatch C:\Users\Rylan\Documents\HackKstate\PipelineBuilder\pipelines\test/the_pipeline.sh --__loop__ $entry --directoryname $loopname/../the_pipeline/
				let file_counter++
			done

			while [ $(ls -lR $loopname/../the_pipeline/*.done | wc -l) -lt $file_counter ]; do
				sleep 30
			done

			touch $loopname/../forloop1.done
			rm $loopname/../the_pipeline/*.done

			uuid=forloop1
		fi
	sleep 5
done
touch $directoryname/big_boi.done