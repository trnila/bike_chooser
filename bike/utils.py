import re

def clean(s):
    return re.sub(r'\s+', ' ', s).strip()

def normalize_attr(s):
    translation = {
        "Ročník": "Rok", 
        "Modelový rok": "Rok"
    }

    s = clean(s)
    if s in translation:
        return translation[s]

    return s
