import os
import re

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

def Get_Method_Declaration(Widget_Name, New_Widget_Name, Declaration, Add_Class_Name = False):
    D = ""
    
    if not(Is_Constructor(Declaration) or Is_Destructor(Declaration)):
        D += Get_Type_Name(Declaration.return_type) + " " 

    
    if Add_Class_Name:
        D += New_Widget_Name + "_Class::"

    if Is_Constructor(Declaration):
        D += New_Widget_Name + "_Class(" + "Object_Class& Parent, "
    elif Is_Destructor(Declaration):
        if not(Add_Class_Name):
            D += "virtual "
        D += "~" + New_Widget_Name + "_Class("
    else:
        D += Get_Method_Name(Widget_Name, New_Widget_Name, Declaration) + "("

    for i, Argument in enumerate(Declaration.arguments):
        if i == 0 and Is_This_Argument(Argument):
            continue

        D += Get_Type_Name(Argument.decl_type) + " " + Argument.name + ", "

    if D.endswith(", "):
        D = D[:-2]

    return D + ")"

def Get_Method_Definition(Widget_Name, New_Widget_Name, Declaration):
    D = Get_Method_Declaration(Widget_Name, New_Widget_Name, Declaration, True) + "\n{\n"

    if Is_Constructor(Declaration):
        D += "\tLVGL_Pointer = " + Get_Name(Declaration) + "("
    elif Is_Destructor(Declaration):
        D += "\t" + Get_Name(Declaration) + "("
    else:
        D += "\treturn " + Get_Name(Declaration) + "("

    for i, Argument in enumerate(Declaration.arguments):
        if i == 0 and Is_This_Argument(Argument):
            if Is_Constructor(Declaration):
                D += "Parent.Get_LVGL_Pointer(), "
            else:
                D += "LVGL_Pointer, "
            continue

        D += Argument.name + ", "

    if D.endswith(", "):
        D = D[:-2]

    D += ");\n"

    D += "}\n"

    return D
