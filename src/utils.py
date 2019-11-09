def create_shell_file(location, shell_args):
    f = open(location, "w")
    f.write("#!/bin/bash")
    for arg in shell_args:
        f.write("#SBATCH" + arg)
    f.close()

    return location

def write_shell_args(location, cmd_args):
    f = open(location, "a")
    f.write("while [ "$1" != "" ]; do\n\tcase $1 in\n")
    for arg in cmd_args:
        f.write("\t\t" + arg + ")\t\tshift\n\t\t\t\t" + arg  + "=$1\n\t\t\t\t;;")
    f.write("\tesac\n\tshift\ndone")
    f.close()