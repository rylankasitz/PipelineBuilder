#!/bin/bash
#SBATCH--time=1:00

while [ "$1" != "" ]; do
	case $1 in
		--directoryName) shift
					directoryName=$1
					;;
		--otherDirectoryName) shift
					otherDirectoryName=$1
					;;
		--foundDirectories) shift
					foundDirectories=$1
					;;
	esac
	shift
done

ls $directoryName $otherDirectoryName >> $foundDirectories
