
def scrub_locals(locals):
    locals.pop('self')
    return locals
