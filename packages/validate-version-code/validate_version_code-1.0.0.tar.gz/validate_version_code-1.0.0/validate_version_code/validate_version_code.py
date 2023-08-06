import re

def validate_version_code(version_code:str)->bool:
    """Return a boolean representing if given version code is valid.
        version_code:str, the version code to validate.
    """
    return bool(re.compile(r"\d+\.\d+\.\d+").match(version_code))