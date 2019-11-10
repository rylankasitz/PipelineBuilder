module load Python/3.6.6-foss-2018b
module load Tkinter/3.6.6-foss-2018b-Python-3.6.6
source ~/virtualenvs/tkinter/bin/activate
export PYTHONDONTWRITEBYTECODE=1

program_name=$1

mkdir -p ./programs

srun --nodes=1 --time=1:00:00 --mem=1G --pty --x11 python -m ./src/block_creator_gui.py