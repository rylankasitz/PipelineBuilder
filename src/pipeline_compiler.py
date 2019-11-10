import utils
import sys
import configs.pipeline_config
import configs.program_config
import json_loader
import os

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
        self.pipeline_location = ""
        self.inputs = {}

    def add_input(self, uuid, out):
        if uuid in self.inputs:
            self.inputs[uuid].append(out)
        else:
            self.inputs[uuid] = [out]


def compile_(env, block):
    return {
        "pipeline": compile_pipeline,
        "program": compile_program,
        "loop": compile_loop,
    }[block.type](env, block)

def compile_pipeline(env, pipe):
    shell = utils.get_shell_args(['directoryname'] + [output.output_name for output in pipe.outputs])

    for out in pipe.outputs:
        out.output_name = "$"+out.output_name
        env.add_input(out.input_uuid, out)

    setup_constants(env, (b for _, b in pipe.blocks.items() if b.type == "constant"))

    file_ = env.pipeline_location + "/" + pipe.name + ".sh"
    steps = len(pipe.blocks)

    shell += '\n\nstep=0\nuuid="init"\ntouch $directoryname/$uuid.done\n\n'
    shell += 'while [ "$step" -lt "' + str(steps) + '" ]; do\n\tfile=$directoryname/$uuid.done'

    for block in flatten_blocks(pipe.blocks):
        compiled = compile_(env, block)
        shell += '\n\t\tif [ -f "$file" ]\n\t\tthen\n\t\t\t' + compiled + "\n\t\t\tuuid=" + block.uuid + "\n\t\tfi"

    shell += "\n\tsleep 5\ndone"
    shell += "\ntouch $directoryname/" + pipe.uuid + ".done"

    utils.create_shell_file(file_, []) # add shell args later
    utils.export_path_in_shell(file_, '$(realpath "/pipelines/' + pipe.name + '")')
    utils.append_to_file(file_, shell)

    return ""

def compile_program(env, block):
    program_block = utils.get_block(block.name)

    def gen_inputs():
        for input_ in env.inputs[block.uuid]:
            arg = "--{} {}".format(input_.input_name, input_.output_name)
            yield arg

    def gen_outputs():
        for out in block.outputs:
            output_type = program_block.output_types[out.output_name]
            output_file = "$directoryname/" + block.name + output_type
            arg = "--{} {}".format(
                out.output_name,
                output_file
            )
            out.output_name = output_file
            env.add_input(out.input_uuid, out)
            yield arg

    args =  " ".join(gen_inputs()) + " " + " ".join(gen_outputs())
    line = "sbatch {}/run_{}.sh {}".format(env.program_location, block.name, args)
    return line

def compile_loop(env, loop):
    def gen_inputs():
        for input_ in env.inputs[loop.uuid]:
            arg = "loopname={}".format(input_.output_name)
            yield arg

    progs = flatten_blocks(loop.body.blocks)
    last_prog = progs[len(progs) - 1]
    output_shell = "$loopname/../" + loop.body.name + "/"
    shell = next(gen_inputs())
    shell += "\n\t\t\tfile_counter=0\n\n\t\t\tfor entry in $loopname/" + loop.mapping + "\n\t\t\tdo\n"
    shell += "\t\t\t\tmkdir -p " + output_shell + "$file_counter"
    shell += "\n\t\t\t\tsbatch " + env.pipeline_location + "/" + loop.body.name + ".sh --__loop__ $entry " 
    shell += "--directoryname " + output_shell
    shell += "\n\t\t\t\tlet file_counter++\n\t\t\tdone\n"
    shell += '\n\t\t\twhile [ $(ls -lR ' + output_shell + '*.done | wc -l) -lt $file_counter ]; do\n\t\t\t\tsleep 30\n\t\t\tdone\n'
    shell += "\n\t\t\ttouch $loopname/../" + loop.uuid + ".done\n"
    shell += "\t\t\trm " + output_shell + "*.done\n"

    for out in loop.outputs:
        out.output_name = output_shell
        env.add_input(out.input_uuid, out)
    
    compile_(env, loop.body)

    return shell

def flatten_blocks(blocks):
    new_blocks = list()
    for key, block in blocks.items():
        if block.type != "constant":
            new_blocks.append(block)
    new_blocks.sort(key=lambda val: val.run_order)
    return new_blocks

def setup_constants(env, constants):
    for const in constants:
        for out in const.outputs:
            env.add_input(out.input_uuid, out)

#pipeline = utils.get_pipeline("test")



#utils.pretty_print(utils.convert_to_dict(pipeline))

pipeline_name = "test"

env = Env()
env.directory = "dir"
env.program_location = os.path.abspath("./programs")
env.pipeline_location = os.path.abspath("./pipelines/" + pipeline_name)

prog = json_loader.load_config("pipelines/test/config.json")

add_excecution_order(prog.blocks, prog.outputs, 0)

compile_(env, prog)

