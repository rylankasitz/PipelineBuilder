import sys
import os

import utils
import configs.program_config as program_config
import json_loader

program_name = sys.argv[1]
program = utils.get_block(program_name)

file_name = os.path.dirname(os.path.abspath(__file__)) + "\\..\\programs\\run_" + program_name + ".sh"
utils.create_shell_file(file_name, program.sbatch)
utils.write_shell_args(file_name, program.inputs + program.outputs)
utils.append_to_file(file_name, "\n\n" + program.command + "\n")