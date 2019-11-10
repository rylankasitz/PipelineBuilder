#!/bin/bash

while [ "$1" != "" ]; do
	case $1 in
		--directoryname) shift
					directoryname=$1
					;;
		--__loop__) shift
					__loop__=$1
					;;
	esac
	shift
done

step=0
uuid="init"
mkdir -p $directoryname/.steps
touch $directoryname/.steps/$uuid.done

while [ "$step" -lt "2" ]; do
	file=$directoryname/.steps/$uuid.done
	if [ -f "$file" ]
	then
		rm $directoryname/.steps/$uuid.done
		if [ "$step" == 0 ]
		then
			sbatch C:\Users\Rylan\Documents\HackKstate\PipelineBuilder\programs/run_add_count.sh --input $__loop__ --count 100 --output $directoryname/add_count.txt --done $directoryname/.steps/program1.done
			uuid=program1
		fi
		if [ "$step" == 1 ]
		then
			sbatch /homes/rylankasitz/PipelineBuilder/programs/run_add_count.sh --count 50 --input $directoryname/add_count.txt --final_output $directoryname/final_output --done $directoryname/.steps/program2.done
			uuid=program2
		fi
		let "step++"
	fi
	sleep 1
done
touch $directoryname/pipeline1.done