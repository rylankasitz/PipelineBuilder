import os
import json_loader
import configs.program_config
import configs.pipeline_config
import pprint

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

def export_path_in_shell(file_, path):
    append_to_file(file_, 'export PATH="' + path + ':$PATH"\n\n')

def get_pipeline(name):
    config_file = os.path.dirname(os.path.abspath(__file__)) + "\\..\\pipelines\\" + name + "\\config.json"
    return json_loader.load_config(config_file)

def get_blocks():
    config_file = os.path.dirname(os.path.abspath(__file__)) + "\\..\\programs\\blocks.json"
    return json_loader.load_config(config_file) 

def get_block(name):
    return get_blocks()[name]

def convert_to_dict(obj):
    if hasattr(obj, "__dict__"):
        return convert_to_dict(obj.__dict__)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = convert_to_dict(v)
        return obj
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            obj[i] = convert_to_dict(v)
        return obj
    else:
        return obj

def pretty_print(dict_):
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(dict_)


