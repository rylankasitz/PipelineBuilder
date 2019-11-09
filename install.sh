#!/bin/bash

module load Python/3.6.6-foss-2018b
module load Tkinter/3.6.6-foss-2018b-Python-3.6.6

dir=$(dirname "$0")

mkdir -p $dir/virtualenvs/python36
mkdir -p $dir/pipelines
mkdir -p $dir/programs

virtualenv $dir/virtualenvs/python36
source $dir/virtualenvs/python36/bin/activate
export PYTHONDONTWRITEBYTECODE=1

pip install pygubu