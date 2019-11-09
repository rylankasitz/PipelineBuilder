class Program():
    block_type = "program"
    name = ""
    outputs = {}

class Constant():
    block_type = "constant"
    value = ""
    outputs = {}

class ForLoop():
    block_type = "forloop"
    mapping = ""
    outputs = {}
    body = {}