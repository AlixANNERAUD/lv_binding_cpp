import os
import re
from pygccxml import declarations
from pygccxml.declarations import type_traits as Type_Traits
import inspect

def Get_Name(Declaration):
    return Declaration.name

def Get_Type_Name(Declaration):
    if Declaration.decl_string.startswith("::"):
        return Declaration.decl_string.replace("::", "")
    return Declaration.decl_string

def Get_Method_Name(Widget_Name, New_Widget_Name, Declaration):

    Method_Name = Get_Name(Declaration).replace("lv_" + Widget_Name + "_", "")

    return re.sub(r"(^|_)([a-z])", lambda m: m.group(1) + m.group(2).upper(), Method_Name)

def Is_This_Argument(Argument):
    return "lv_obj_t*" in Get_Type_Name(Argument.decl_type).replace(" ", "").replace("const", "")
    
def Is_Constructor(Declaration):
    return Get_Name(Declaration).endswith("create")

def Is_Destructor(Declaration):
    return Get_Name(Declaration).endswith("del")

def Is_Pointer(Declaration):
    return type(Declaration) == declarations.cpptypes.pointer_t

def Is_Constant(Declaration):
    return type(Declaration) == declarations.cpptypes.const_t

def Is_Elabored_Type(Declaration):
    return Type_Traits.is_elaborated(Declaration)

def Is_Declarated(Declaration):
    return type(Declaration) == declarations.cpptypes.declarated_t

#def Convert_To_New_Type(Declaration):

