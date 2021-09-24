import inspect 

def scrub_locals(locals):
    locals.pop('self')
    return locals

def arg_list(fn):
    return list(inspect.signature(fn).parameters.keys())
