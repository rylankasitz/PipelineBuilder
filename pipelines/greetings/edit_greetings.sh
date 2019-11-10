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
			sbatch /homes/rylankasitz/PipelineBuilder/programs/run_say_hello.sh --to_who $__loop__ --output $directoryname/say_hello.txt --done $directoryname/.steps/create_greeting.done
			uuid=create_greeting
		fi
		if [ "$step" == 1 ]
		then
			sbatch /homes/rylankasitz/PipelineBuilder/programs/run_make_letter.sh --greeting $directoryname/say_hello.txt --output $directoryname/make_letter.txt --done $directoryname/.steps/create_letter.done
			uuid=create_letter
		fi
		let "step++"
	fi
	sleep 1
done
touch $directoryname/../$(uuidgen).done