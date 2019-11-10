import sys
import os

import utils
import json_loader

program_name = sys.argv[1]
program = utils.get_block(program_name)

file_name = os.path.dirname(os.path.abspath(__file__)) + "\\..\\programs\\run_" + program_name + ".sh"
utils.create_shell_file(file_name, program.sbatch)
utils.export_path_in_shell(file_name, program.location)
utils.write_shell_args(file_name, ['done'] + program.inputs + program.outputs)
utils.append_to_file(file_name, "\n\n" + program.command + "\n")
utils.append_to_file(file_name, "\ntouch $done")