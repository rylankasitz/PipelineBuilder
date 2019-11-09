def create_shell_file(location, shell_args):
    f = open(location, "a")
    f.write("#!/bin/bash")
    for arg in shell_args:
        f.write("#SBATCH" + arg)
    f.close()