from pygccxml import utils
from pygccxml import declarations as Declarations
from pygccxml import parser as Parser

import Basics
import Paths

import os

Widgets_List = [["obj","Object"],
                #["obj_has","?"],
                #["obj_get","?"],
                ["img","Image"],
                ["animimg","Animated_Image"],
                ["arc","Arc"],
                ["label","Label"],
                ["bar","Bar"],
                ["btn","Button"],
                ["btnmatrix","Button_Matrix"],
                ["calendar","Calendar"],
                ["calendar_header_arrow","Calendar_Header_Arrow"],
                ["calendar_header_dropdown","Calendar_Header_Dropdown"],
                ["canvas","Canvas"],
                ["chart","Chart"],
                ["checkbox","Checkbox"],
                ["colorwheel","Colorwheel"],
                ["dropdown","Dropdown"],
                ["dropdownlist","Dropdown_List"],
                ["imgbtn","Image_Button"],
                ["keyboard","Keyboard"],
                ["led","LED"],
                ["line","Line"],
                ["list","List"],
                ["list_text","List_Text"],
                ["list_btn","List_Button"],
                ["menu","Menu"],
                ["menu_page","Menu_Page"],
                ["menu_cont","Menu_Content"],
                ["menu_section","Menu_Section"],
                ["menu_separator","Menu_Separator"],
                ["menu_sidebar_cont","Menu_Sidebar_Content"],
                ["menu_main_cont","Menu_Main_Content"],
                ["menu_sidebar_header_cont","Menu_Sidebar_Header_Content"],
                ["menu_main_header_cont","Menu_Main_Header_Content"],
                ["meter","Meter"],
                ["msgbox","Message_Box"],
                ["msgbox_content","Message_Box_Content"],
                ["msgbox_backdrop","Message_Box_Backdrop"],
                ["roller","Roller"],
                ["slider","Slider"],
                ["spangroup","Span_Group"],
                ["textarea","Text_Area"],
                ["spinbox","Spinbox"],
                ["spinner","Spinner"],
                ["switch","Switch"],
                ["table","Table"],
                ["tabview","Tabview"],
                ["tileview","Tileview"],
                ["tileview_tile","Tileview_Tile"],
                ["win", "Window"]]


def Generate_All_Bindings(Global_Namespace):
    for Widget in Widgets_List:
        Generate_Bindings(Widget[0], Widget[1], Global_Namespace)


def Open_Header_File(Widget_Name):
    return open(os.path.join(Paths.Get_Bindings_Header_Path(), Widget_Name + ".hpp"), "w")

def Open_Source_File(Widget_Name):
    return open(os.path.join(Paths.Get_Bindings_Source_Path(), Widget_Name + ".cpp"), "w")

def Get_Class_Name(Widget_Name):
    return "" + Widget_Name + "_Class"

def Get_Type_Name(Widget_Name):
    return "" + Widget_Name + "_Type"

def Write_Header_Header(Widget_Name, File):
    File.write("#pragma once\n")
    File.write("#include <memory>\n")
    File.write("#include \"lvgl.h\"\n\n")
    if Widget_Name != "Object":
        File.write("#include \"Object.hpp\"\n\n")
        
    File.write("namespace LVGL\n")
    File.write("{\n")
    File.write("    typedef class " + Get_Class_Name(Widget_Name))
    if Widget_Name != "Object":
        File.write(" : public Object_Class")

    File.write("\n\t{\n")
    File.write("    public:\n")

def Write_Header_Footer(Widget_Name, File):
    File.write("    } " + Get_Type_Name(Widget_Name) + ";\n")
    File.write("}\n")
    
def Write_Source_Header(Widget_Name, File):
    File.write("#include \"" + Widget_Name + ".hpp\"\n\n")
    File.write("using namespace LVGL;\n\n")

def Write_Source_Footer(Widget_Name, File):
    pass

def Get_New_Widget_Name(Widget_Name):
    for Widget in Widgets_List:
        if Widget[0] == Widget_Name:
            return Widget[1]
    return None

def Get_Method_Declaration(Widget_Name, New_Widget_Name, Declaration, Add_Class_Name = False):
    D = ""
    
    if not(Basics.Is_Constructor(Declaration) or Basics.Is_Destructor(Declaration)):
        print(str(Declaration.return_type) + " : " + str(type(Declaration.return_type)))
        if Basics.Is_Pointer(Declaration.return_type):
            Base = Declaration.return_type.base
            print("base : ", str(Base))
            if Basics.Is_Constant(Base):
                D += "const "
                Base = Base.base


            print("base : ", str(type(Base)))

            if Basics.Is_Declarated(Base):
                Declaration_String = Base.declaration.decl_string.replace("::", "").replace("lv_", "").replace("_t", "")
                New_Type_Name = Get_New_Widget_Name(Declaration_String)
                if New_Type_Name == None:
                    D += Base.decl_string + "* "
                else:
                    D += New_Type_Name + "* "
            else:
                D += Basics.Get_Type_Name(Base) + "& "
                

            D += Basics.Get_Type_Name(Base) + "* "

    
        else:
            D += Basics.Get_Type_Name(Declaration.return_type) + " " 


    if Add_Class_Name:
        D += New_Widget_Name + "_Class::"

    if Basics.Is_Constructor(Declaration):
        D += New_Widget_Name + "_Class(" + "Object_Class& Parent, "
    elif Basics.Is_Destructor(Declaration):
        if not(Add_Class_Name):
            D += "virtual "
        D += "~" + New_Widget_Name + "_Class("
    else:
        D += Basics.Get_Method_Name(Widget_Name, New_Widget_Name, Declaration) + "("

    for i, Argument in enumerate(Declaration.arguments):
        if i == 0 and Basics.Is_This_Argument(Argument):
            continue

        D += Basics.Get_Type_Name(Argument.decl_type) + " " + Argument.name + ", "

    if D.endswith(", "):
        D = D[:-2]

    return D + ")"

def Get_Method_Definition(Widget_Name, New_Widget_Name, Declaration):
    D = Get_Method_Declaration(Widget_Name, New_Widget_Name, Declaration, True) + "\n{\n"

    if Basics.Is_Constructor(Declaration):
        D += "\tLVGL_Pointer = " + Basics.Get_Name(Declaration) + "("
    elif Basics.Is_Destructor(Declaration):
        D += "\t" + Basics.Get_Name(Declaration) + "("
    else:
        if type(Declaration.return_type) == Declarations.cpptypes.void_t:
            D += "\t" + Basics.Get_Name(Declaration) + "("
        else:    
            D += "\treturn " + Basics.Get_Name(Declaration) + "("

    for i, Argument in enumerate(Declaration.arguments):
        if i == 0 and Basics.Is_This_Argument(Argument):
            if Basics.Is_Constructor(Declaration):
                D += "Parent.Get_LVGL_Pointer(), "
            else:
                D += "LVGL_Pointer, "
            continue

        D += Argument.name + ", "

    if D.endswith(", "):
        D = D[:-2]

    D += ");\n"

    if Basics.Is_Destructor(Declaration):
        D += "\tClear_Pointer();\n"

    D += "}\n"

    return D

def Generate_Bindings(Widget_Name, New_Widget_Name, Global_Namespace):

    # - Header
    Header_File = Open_Header_File(New_Widget_Name)

    Write_Header_Header(New_Widget_Name, Header_File)

    # - - Methods

    for Declaration in Global_Namespace.free_functions():
        if Basics.Get_Name(Declaration).startswith("lv_" + Widget_Name):
            Header_File.write("\t\t" + Get_Method_Declaration(Widget_Name, New_Widget_Name, Declaration) + ";\n")
    
    if New_Widget_Name == "Object":
        Header_File.write("\t\tinline " + New_Widget_Name + "_Class() : LVGL_Pointer(NULL) { };\n")
        Header_File.write("\t\tinline lv_obj_t* Get_LVGL_Pointer() const { return LVGL_Pointer; };\n")
        Header_File.write("\t\tinline void Clear_Pointer() { LVGL_Pointer = NULL; };\n")

    Header_File.write("\n")

    # - - Attributes

    Header_File.write("\t\tstatic const lv_obj_class_t& Class;\n")

    if New_Widget_Name == "Object":
        Header_File.write("\tprotected:\n")
        Header_File.write("\t\tlv_obj_t* LVGL_Pointer;\n")

    Write_Header_Footer(New_Widget_Name, Header_File)

    Header_File.close()

    # - Source

    Source_File = Open_Source_File(New_Widget_Name)

    Write_Source_Header(New_Widget_Name, Source_File)

    # - - Attributes

    Source_File.write(f"const lv_obj_class_t& {Get_Class_Name(New_Widget_Name)}::Class = lv_{Widget_Name}_class;\n\n")

    # - - Methods

    for Declaration in Global_Namespace.free_functions():

        if Basics.Get_Name(Declaration).startswith("lv_" + Widget_Name):
            Source_File.write(Get_Method_Definition(Widget_Name, New_Widget_Name, Declaration) + "\n\n")

    Write_Source_Footer(New_Widget_Name, Source_File)

    Source_File.close()


    print ("=== Variables")
    for Declaration in Global_Namespace.variables():
        if Basics.Get_Name(Declaration).startswith("lv_" + Widget_Name):
            print(Basics.Get_Name(Declaration))