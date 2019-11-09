import sys
import os

import utils
import configs.program_config as program_config

program_name = sys.argv[1]

# test data
program = program_config.ProgramBlock()
program.block_name = "test"
program.command = "python test.py $one -t $two > $three"
program.inputs = ["one", "two"]
program.outputs = ["three"]
program.sbatch = ["--time=1-00:00:00"]

file_name = os.path.dirname(os.path.abspath(__file__)) + "\\..\\programs\\" + program_name + "\\run_" + program_name + ".sh"
utils.create_shell_file(file_name, program.sbatch)
utils.write_shell_args(file_name, program.inputs + program.outputs)
utils.append_to_file(file_name, "\n\n" + program.command + "\n")