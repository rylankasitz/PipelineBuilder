from json_loader import register

@register("program_block")
class ProgramBlock():
    name = ""
    command = ""
    inputs = list()
    outputs = list()
    sbatch = {}
    output_types = {}
