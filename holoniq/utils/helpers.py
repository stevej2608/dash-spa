import inspect

def arg_list(fn):
    return list(inspect.signature(fn).parameters.keys())


def calling_module():
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    return mod


def calling_module_name():
    mod = calling_module()
    return mod.__name__
