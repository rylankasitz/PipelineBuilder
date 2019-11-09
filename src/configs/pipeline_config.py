from json_loader import register

@register("output")
class Outputs():
    input_uuid = ""
    output_name = ""
    input_name = ""

@register("pipeline")
class Pipeline():
    blocks = {}
    outputs = []

@register("program")
class Program():
    name = ""
    outputs = []

@register("constant")
class Constant():
    value = ""
    outputs = []

@register("forloop")
class ForLoop():
    mapping = ""
    outputs = []
    body = {}
