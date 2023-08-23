from pygccxml import utils
from pygccxml import declarations
from pygccxml import parser as Parser

import Type

import re

class Variable_Class():
    
    def __init__(self, Type, Name):
        self.Type = Type
        self.Name = Name

    def Get_Name(self):
        return self.Name

    def Get_New_Name(self):
        return re.sub(r"(^|_)([a-z])", lambda m: m.group(1) + m.group(2).upper(), self.Name)

    def Get_Type(self):
        return self.Type    
