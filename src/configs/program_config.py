from json_loader import register

@register("program_block")
class ProgramBlock():
    name = ""
    command = ""
    location = ""
    inputs = list()
    outputs = list()
    sbatch = list()
    output_types = {}
