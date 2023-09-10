from pygccxml import utils
from pygccxml import declarations
from pygccxml import parser as Parser

import re

import Type

import Casing

class Variable_Class():
    
    def __init__(self, Type, Name):
        self.Type = Type
        self.Name = Name

    def Get_Name(self):
        return self.Name

    def Get_New_Name(self):
        return Casing.Convert_Alix_Casing(self.Get_Name())

    def Get_Type(self):
        return self.Type    
