from json_loader import register

@register("pipeline")
class Pipeline():
    blocks = {}
    arg_names = {}
    outputs = {}

@register("program")
class Program():
    name = ""
    outputs = {}
    
@register("constant")
class Constant():
    value = ""
    outputs = {}

@register("forloop")
class ForLoop():
    mapping = ""
    outputs = {}
    body = {}
