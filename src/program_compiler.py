import sys
import os

import utils
import json_loader

def run(name):
    program_name = name
    program = utils.get_block(program_name)
    print(program)

    file_name = os.path.abspath("../programs/" + "run_" + program_name + ".sh")
    utils.create_shell_file(file_name, program.sbatch)
    utils.write_shell_args(file_name, ['done'] + program.inputs + program.outputs)
    utils.append_to_file(file_name, "\n\n" + program.command + "\n")
    utils.append_to_file(file_name, "\ntouch $done")
