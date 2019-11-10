#!/bin/bash

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
mkdir -p $directoryname/.steps
touch $directoryname/.steps/$uuid.done

while [ "$step" -lt "1" ]; do
	file=$directoryname/.steps/$uuid.done
	if [ -f "$file" ]
	then
		rm $directoryname/.steps/$uuid.done
		if [ "$step" == 0 ]
		then
			loopname=$input
			file_counter=0

			for entry in $loopname/*_greet.txt
			do

				sbatch /homes/rylankasitz/PipelineBuilder/pipelines/greetings/edit_greetings.sh --__loop__ $entry --directoryname $loopname/../edit_greetings_$file_counter/
				let file_counter++
			done

			while [ $(ls -lR $loopname/../*.done | wc -l) -lt $file_counter ]; do
				sleep 1
			done

			touch $directoryname/.steps/loop.done
			rm $loopname/../*.done

			uuid=loop
		fi
		let "step++"
	fi
	sleep 1
done
touch $directoryname/../$(uuidgen).done