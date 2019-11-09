import utils
import sys

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

def compile_(block):
    return {
        "pipeline": compile_pipeline,
        "program": compile_program,
        "loop": compile_loop,
        "constant": compile_constant,
    }[block.type](block)

def compile_pipeline(pipe):
    utils.create_shell_file("name_of_some_sort")
    utils.write_shell_args("do_args")
    for b in pipe.blocks:
        compile_(b)
    # ending stuff

def compile_program(block, env):
    program_block = utils.get_block(block.name)

    def gen_outputs():
        for out in block.outputs:
            output_type = program_block.output_types[out.output_name]
            arg = "--{} {}/../{}{}".format(
                out.output_name,
                env.directory,
                block.name,
                output_type
            )
            yield arg

    args = " ".join(gen_outputs())
    line = "sbatch {}/{}.sh {} {}".format(env.program_location, block.name, "",args)

def compile_loop():
    pass

def compile_constant():
    pass
pipeline = utils.get_pipeline("test")

add_excecution_order(pipeline.blocks, pipeline.outputs, 0)

utils.pretty_print(utils.convert_to_dict(pipeline))
