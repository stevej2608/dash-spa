import os
from dotenv import load_dotenv

load_dotenv()

def getenv(id, default=None):
    """Get an environment variable, return None if it doesn't exist.
    The optional second argument can specify an alternate default.
    key, default and the result are str."""
    
    return os.getenv(id, default=default)
