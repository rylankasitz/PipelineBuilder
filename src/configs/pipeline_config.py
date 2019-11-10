from json_loader import register

@register("output")
class Outputs():
    input_uuid = ""
    output_name = ""
    input_name = ""

@register("pipeline")
class Pipeline():
    uuid = ""
    name = ""
    blocks = {}
    outputs = []

@register("program")
class Program():
    uuid = ""
    name = ""
    outputs = []

@register("constant")
class Constant():
    value = ""
    outputs = []

@register("loop")
class Loop():
    uuid = ""
    mapping = ""
    outputs = []
    body = {}
