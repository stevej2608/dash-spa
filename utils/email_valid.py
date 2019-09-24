import re

def email_valid(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)