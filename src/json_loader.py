import json

_TYPE_KEY = "type"
_REGISTERED_CLASSES = {}

def register(block_type):
    def wrapper(cls):
        setattr(cls, _TYPE_KEY, block_type)
        _REGISTERED_CLASSES[block_type] = cls
        return cls
    return wrapper

def load_config(file_name):
    with open(file_name) as fp:
        loaded = json.load(fp)
    return loaded

def load_block(config_dict):
    if _TYPE_KEY in config_dict:
        block_type = config_dict[_TYPE_KEY]
        block_class = _REGISTERED_CLASSES[block_type]
        attribs = [a for a in dir(block_class) if not (a.startswith('__') and a.endswith('__'))]
        instance = block_class()
        for a in attribs:
            setattr(instance, a, load_block(config_dict[a]))
        return instance
    elif isinstance(config_dict, dict):
        return [load_block(x) for x in config_dict]
    elif isinstance(config_dict, list):
        return [load_block(x) for x in config_dict]
    else:
        config_dict

def write_block(block):
    return block.__dict__

def write_config(file_name, config):
    for k, v in config.items():
        config[k] = write_block(v)

    with open(file_name, "w") as fp:
        json.dump(config, fp)

