import utils
import sys
import configs.pipeline_config
import configs.program_config
import json_loader

def add_excecution_order(blocks, outputs, run_num):
    for output in outputs:
        if not hasattr(blocks[output.input_uuid], "run_order"):
            blocks[output.input_uuid].run_order = 0

        if blocks[output.input_uuid].type == "loop":
            add_excecution_order(blocks[output.input_uuid].body.blocks, blocks[output.input_uuid].body.outputs, 0)

        blocks[output.input_uuid].run_order = max(blocks[output.input_uuid].run_order, run_num + 1)
        add_excecution_order(blocks, blocks[output.input_uuid].outputs, run_num + 1)

class Env:
    def __init__(self):
        self.directory = ""
        self.program_location = ""
        self.inputs = {}

def compile_(env, block):
    return {
        "pipeline": compile_pipeline,
        "program": compile_program,
        "loop": compile_loop,
        "constant": compile_constant,
    }[block.type](block)

def compile_pipeline(env, pipe):
    for b in pipe.blocks:
        compile_(b)
    # ending stuff

def compile_program(env, block):
    program_block = utils.get_block(block.name)

    def gen_inputs():
        for input_ in env.inputs[block.uuid]:
            arg = "--{} {}".format(input_.input_name, input_.output_name)
            yield arg

    def gen_outputs():
        for out in block.outputs:
            output_type = program_block.output_types[out.output_name]
            arg = "--{} {}/../{}{}".format(
                out.output_name,
                env.directory,
                block.name,
                output_type
            )
            env.inputs[out.input_uuid] = out
            yield arg

    args =  " ".join(gen_inputs()) + " " + " ".join(gen_outputs())
    line = "sbatch {}/run_{}.sh {}".format(env.program_location, block.name, args)
    print(line)

def compile_loop(env, loop):
    pass

def compile_constant(env, constant):
    pass

#pipeline = utils.get_pipeline("test")

#add_excecution_order(pipeline.blocks, pipeline.outputs, 0)

#utils.pretty_print(utils.convert_to_dict(pipeline))


env = Env()
env.directory = "dir"
env.program_location = "progs"

a = configs.pipeline_config.Outputs()
a.input_uuid = "program1"
a.output_name = "some_outputed_file.txt"
a.input_name = "input"

b = configs.pipeline_config.Outputs()
b.input_uuid = "program1"
b.output_name = "some_count_file.txt"
b.input_name = "count"

env.inputs = {
    "program1": [a, b]
}

prog = json_loader.load_config("pipelines/test/program_config.json")

compile_program(env, prog)

