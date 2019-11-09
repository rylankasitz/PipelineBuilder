class Program():
    self.block_type = "program"
    self.name = ""
    self.outputs = {}

class Constant():
    self.block_type = "constant"
    self.value = ""
    self.outputs = {}

class ForLoop():
    self.block_type = "forloop"
    self.mapping = ""
    self.outputs = {}
    self.body = {}