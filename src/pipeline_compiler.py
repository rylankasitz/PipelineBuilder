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
    }[block.type](env, block)

def compile_pipeline(env, pipe):
    for out in pipe.outputs:
        if out.input_uuid in env.inputs:
            env.inputs[out.input_uuid].append(out)
        else:
            env.inputs[out.input_uuid] = [out]

    steps = len(pipe.blocks)
    shell = utils.get_shell_args(['directoryname'] + [output.output_name for output in pipe.outputs])
    shell += 'step=0\nuuid="init"\ntouch $directoryname/../$uuid.done\n\n'
    shell += 'while [ "$step" -lt "' + str(steps) + '" ]; do\n\tfile=$directoryname/../$uuid.done'
    for uuid, block in pipe.blocks.items():
        compiled = compile_(env, block)
        print(compiled)
        shell += '\n\t\tif [ -f "$file" ]\n\t\tthen\n\t\t\t' + compiled + "\n\t\t\tuuid=" + uuid + "\n\t\tfi"
    shell += "\n\tsleep 5\ndone"
    shell += "\ntouch $directoryname/../<pipeline_uuid>.done"
    return shell

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
            if out.input_uuid in env.inputs:
                env.inputs[out.input_uuid].append(out)
            else:
                env.inputs[out.input_uuid] = [out]
           
            yield arg

    args =  " ".join(gen_inputs()) + " " + " ".join(gen_outputs())
    line = "sbatch {}/run_{}.sh {}".format(env.program_location, block.name, args)
    return line

def compile_loop(env, loop):
    return ""

def compile_constant(env, constant):
    return ""

#pipeline = utils.get_pipeline("test")

#add_excecution_order(pipeline.blocks, pipeline.outputs, 0)

#utils.pretty_print(utils.convert_to_dict(pipeline))


env = Env()
env.directory = "dir"
env.program_location = "progs"

prog = json_loader.load_config("pipelines/test/test.json")

print(compile_(env, prog))

