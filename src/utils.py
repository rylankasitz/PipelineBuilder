def create_shell_file(file_, shell_args):
    f = open(file_, "w+")
    f.write("#!/bin/bash\n")
    for arg in shell_args:
        f.write("#SBATCH" + arg + "\n")
    f.write("\n")
    f.close()

def write_shell_args(file_, cmd_args):
    f = open(file_, "a")
    f.write('while [ "$1" != "" ]; do\n\tcase $1 in\n')
    for arg in cmd_args:
        f.write("\t\t--" + arg + ") shift\n\t\t\t\t\t" + arg  + "=$1\n\t\t\t\t\t;;\n")
    f.write("\tesac\n\tshift\ndone")
    f.close()

def append_to_file(file_, text):
    f = open(file_, "a")
    f.write(text)
    f.close()