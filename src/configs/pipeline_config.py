from json_loader import register

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