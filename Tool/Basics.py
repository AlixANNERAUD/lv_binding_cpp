import os
import re
from pygccxml import declarations
from pygccxml.declarations import type_traits as Type_Traits
import inspect

import Paths

def Open_Main_Header_File():
    return open(os.path.join(Paths.Get_Bindings_Header_Path(), "LVGL_Cpp.hpp"), "w")

def Get_Name(Declaration):
    return Declaration.name

def Get_Method_Name(Widget_Name, New_Widget_Name, Declaration):

    Method_Name = Get_Name(Declaration).replace("lv_" + Widget_Name + "_", "")

    return re.sub(r"(^|_)([a-z])", lambda m: m.group(1) + m.group(2).upper(), Method_Name)

def Is_Elabored_Type(Declaration):
    return Type_Traits.is_elaborated(Declaration)

#def Convert_To_New_Type(Declaration):

