import inspect

def arg_list(fn):
    return list(inspect.signature(fn).parameters.keys())
