import re

def Convert(Word: str) -> str:
    return Convert_Alix_Casing(Word)

def Convert_Alix_Casing(Word : str) -> str:
    return re.sub(r"(^|_)([a-z])", lambda m: m.group(1) + m.group(2).upper(), Word)

def Convert_Snake_Casing(Word : str) -> str:
    return re.sub(r"(^|_)([A-Z])", lambda m: m.group(1) + m.group(2).lower(), Word)