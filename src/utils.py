import os
import json_loader
import configs.program_config
import configs.pipeline_config
import pprint


def get_pipeline(name):
    config_file = os.path.dirname(os.path.abspath(__file__)) + "/../pipelines/" + name + "/config.json"
    return json_loader.load_config(config_file)

def get_blocks():
    config_file = os.path.dirname(os.path.abspath(__file__)) + "/../programs/blocks.json"
    return json_loader.load_config(config_file) 

def get_block(name):
    return get_blocks()[name]

def pretty_print(dict_):
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(dict_)


