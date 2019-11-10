program_name=$1

mkdir -p ./programs

srun --nodes=1 --time=1:00:00 --mem=1G --pty --x11 python -m ./src/block_creator_gui.py

./src/pipeline_compiler.py $program_name