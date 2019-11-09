#!/bin/bash
#SBATCH --time=6-00:00:00   # Use the form DD-HH:MM:SS
#SBATCH --output=minion.out
#SBATCH --error=minion.err

# use util method to create args with list of output names
while [ "$1" != "" ]; do
    case $1 in
        --$directoryname )  shift
                            $directoryname=$1
                            ;;
        --$output_name )    shift
                            $output_name=$1
                            ;;
        # contiue for all outputs of pipeline
    esac
    shift
done

step=0
new_uuid="init"
touch $directoryname/../$uuid.done
program_location=<location of programs>

while [ "$step" -lt <len(blocks) + 1> ]; do
    file=$directoryname/../$uuid.done
    if [ -f "$file" ] 
    then
        rm $directoryname/../$uuid.done
        if [ $step == 0 ]
        then
            # Step 0 program call with mapped outputs
            sbatch $program_location/<program name> [mapped inputs] --<output_name> $directoryname/../<program_nam><extention>
            uuid=<block.uuid>
        fi

        # continue for the rest of the steps

        let "step++"
    fi
    sleep 5
done

touch $directoryname/../<pipeline_uuid>.done