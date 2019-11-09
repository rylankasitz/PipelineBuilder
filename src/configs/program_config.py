from json_loader import register

@register("programblock")
class ProgramBlock():
    name = ""
    command = ""
    inputs = list()
    outputs = list()
    sbatch = list()
