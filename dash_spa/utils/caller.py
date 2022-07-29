import sys
from inspect import getframeinfo, stack

# https://stackoverflow.com/a/24439444/489239

def caller_hash(depth:int=1, prefix:str='#') -> str:
    """Return hash derived from the the call stack filename and location

    Args:
        depth (int, optional): The depth in the call stack. Defaults to 1 (callers caller).
        prefix (str, optional): Prefix for returned hash. Defaults to '#'.

    Returns:
        str: _description_
    """
    caller = getframeinfo(stack()[depth+1][0])
    str = f"{caller.filename}/{caller.lineno}"
    _hash = hash(str)
    _hash += sys.maxsize + 1
    return prefix + hex(_hash)[2:]

