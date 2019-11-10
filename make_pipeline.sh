module load Python/3.6.6-foss-2018b
module load Tkinter/3.6.6-foss-2018b-Python-3.6.6
source /homes/rylankasitz/PipelineBuilder/virtualenvs/python36/bin/activate
export PYTHONDONTWRITEBYTECODE=1

rm ~/.Xauthority-*

pipline_name=$1

mkdir -p ./pipelines/$pipline_name

srun --nodes=1 --time=1:00:00 --mem=1G --pty --x11 python -m ./src/pipeline_gui.py

./src/pipeline_compiler.py $pipline_name