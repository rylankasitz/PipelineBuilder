import sys
import os

import json_loader
import shell_writer
import utils

def run(name):
    program = utils.get_block(name)

    file_name = os.path.abspath("./programs/" + "run_" + name + ".sh")
    contents = shell_writer.program_wrapper(program.sbatch, ['done'] + program.inputs + program.outputs, program.command)
    shell_writer.write(file_name, contents)
    
run('say_hello')
run('make_letter')
