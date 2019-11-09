import json

_TYPE_KEY = "block_type"
_REGISTERED_CLASSES = {}

def register(block_type):
    def wrapper(cls):
        setattr(cls, _TYPE_KEY, block_type)
        _REGISTERED_CLASSES[block_type] = cls
        return cls
    return wrapper

@register("program")
class Config():
    attrib1 = ""
    attrib2 = ""

def load_config(file_name):
    with open(file_name) as fp:
        loaded = json.load(fp)

    for k, v in loaded.items():
        block = load_block(v)
        loaded[k] = block

    return loaded

def load_block(config_dict):
    block_type = config_dict[_TYPE_KEY]
    block_class = _REGISTERED_CLASSES[block_type]
    attribs = [a for a in dir(block_class) if not (a.startswith('__') and a.endswith('__'))]
    instance = block_class()
    for a in attribs:
        setattr(instance, a, config_dict[a])
    return instance

def write_block(block):
    return block.__dict__

def write_config(file_name, config):
    for k, v in config.items():
        config[k] = write_block(v)

    with open(file_name, "w") as fp:
        json.dump(config, fp)

