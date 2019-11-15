import utils
import shell_writer
import sys
import configs.pipeline_config
import configs.program_config
import json_loader
import os

class Env:
    def __init__(self):
        self.directory = ""
        self.program_location = ""
        self.pipeline_location = ""
        self.inputs = {}
        self.workspace = ""

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
    for out in pipe.outputs:
        env.add_input(out.input_uuid, out)

    setup_constants(env, (b for _, b in pipe.blocks.items() if b.type == "constant"))
    file_ = env.pipeline_location + '/' + pipe.name + '.sh'

    shell = shell_writer.pipeline(env.workspace, {}, [env.workspace] + [out.output_name for out in pipe.outputs],
                [compile_(env, block) for block in flatten_blocks(pipe.blocks)])
    shell_writer.write(file_, shell)
    
    if pipe.root == "True": return ""
    
    inputs = {}
    for input_ in env.inputs[pipe.uuid]:
        inputs[input_.output_name] = input_.input_name
        
    return shell_writer.program(env.workspace, file_, inputs, {})

def compile_program(env, block):
    program_block = utils.get_block(block.name)

    inputs = { 'done' : '$' + env.workspace + '/.steps/$uuid.done'}
    for input_ in env.inputs[block.uuid]:
        inputs[input_.input_name] = input_.output_name

    outputs = {}
    for out in block.outputs:
        if out.output_name not in program_block.output_types:
            output_file = out.output_name
        else:
            output_type = program_block.output_types[out.output_name]
            output_file = block.name + output_type
            
        outputs[out.output_name] = output_file
        out.output_name = output_file
        env.add_input(out.input_uuid, out)
        

    return shell_writer.program(env.workspace,
                                '{}/run_{}.sh'.format(env.program_location, block.name), 
                                inputs, outputs)

def compile_loop(env, loop):
    def gen_inputs():
        for input_ in env.inputs[loop.uuid]:
            yield input_.output_name
    
    #for block in flatten_blocks(loop.body.blocks):
    #    add_output(block.uuid, env.workspace + '/.steps/$uuid.done', 'done', loop.body)
        
    add_output(loop.body.uuid, env.workspace,  env.workspace + '/' + loop.body.name + '_$count', loop)
    
    for out in loop.outputs:
        env.add_input(out.input_uuid, out)

    return shell_writer.loop(env.workspace, next(gen_inputs()), loop.mapping, compile_(env, loop.body))

def add_output(input_uuid, output_name, input_name, output_):
    out = configs.pipeline_config.Outputs()
    out.type = 'output'
    out.input_uuid = input_uuid
    out.output_name = output_name
    out.input_name = input_name
    output_.outputs.append(out)
    
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
            
def add_excecution_order(blocks, outputs, run_num):
    for output in outputs:
        if output.input_uuid != None and  output.input_uuid in blocks:
            if not hasattr(blocks[output.input_uuid], "run_order"):
                blocks[output.input_uuid].run_order = 0

            if blocks[output.input_uuid].type == "loop":
                add_excecution_order(blocks[output.input_uuid].body.blocks, blocks[output.input_uuid].body.outputs, 0)

            blocks[output.input_uuid].run_order = max(blocks[output.input_uuid].run_order, run_num + 1)
            add_excecution_order(blocks, blocks[output.input_uuid].outputs, run_num + 1)

def run(pipeline_name):
    env = Env()
    env.directory = "dir"
    env.program_location = os.path.abspath('./programs')
    env.pipeline_location = os.path.abspath('./pipelines/' + pipeline_name)
    env.workspace = 'workspace'

    prog = json_loader.load_config('./pipelines/' + pipeline_name +'/config.json')

    add_excecution_order(prog.blocks, prog.outputs, 0)

    compile_(env, prog)