import os
import re
from pygccxml import declarations
from pygccxml.declarations import type_traits as Type_Traits
import inspect

import Paths

# - Configuration

Library_Namespace = "LVGL"

# - Functions

def Open_Main_Header_File():
    return open(os.path.join(Paths.Get_Bindings_Header_Path(), "LVGL_Cpp.hpp"), "w")

def Get_Name(Declaration):
    return Declaration.name
    
def Is_Elabored_Type(Declaration):
    return Type_Traits.is_elaborated(Declaration)

#def Convert_To_New_Type(Declaration):

