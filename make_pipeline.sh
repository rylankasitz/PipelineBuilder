pipline_name=$1

mkdir -p ./pipelines/$pipline_name

srun --nodes=1 --time=1:00:00 --mem=1G --pty --x11 python -m ./src/pipeline_gui.py $pipline_name

./src/pipeline_compiler.py $pipline_name