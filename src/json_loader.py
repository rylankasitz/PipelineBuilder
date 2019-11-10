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
    return load_block(loaded)

def load_block(config_dict):
    if config_dict is None:
        return None
    elif _TYPE_KEY in config_dict:
        block_type = config_dict[_TYPE_KEY]
        block_class = _REGISTERED_CLASSES[block_type]
        attribs = [a for a in dir(block_class) if not (a.startswith('__') and a.endswith('__'))]
        instance = block_class()
        for a in attribs:
            setattr(instance, a, load_block(config_dict[a]))
        return instance
    elif isinstance(config_dict, dict):
        for k, v in config_dict.items():
            config_dict[k] = load_block(v)
    elif isinstance(config_dict, list):
        return [load_block(x) for x in config_dict]
    return config_dict


def write_block(block):
    return block.__dict__

def write_config(file_name, config):
    converted = convert_to_dict(config)

    with open(file_name, "w") as fp:
        json.dump(converted, fp)

def convert_to_dict(obj):
    if hasattr(obj, "__dict__"):
        return convert_to_dict(obj.__dict__)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = convert_to_dict(v)
        return obj
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            obj[i] = convert_to_dict(v)
        return obj
    else:
        return obj
