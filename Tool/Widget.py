from pygccxml import utils
from pygccxml import declarations as Declarations
from pygccxml import parser as Parser

import Basics
import Paths

import os

import Method
import Type

# Currently ignoring widgets due to ambiguous naming
    



class Widget_Class:

    List = [["obj","Object"],
                #["obj_has","?"],
                #["obj_get","?"],
#                ["img","Image"],
                ["animimg","Animated_Image"],
                ["arc","Arc"],
                ["label","Label"],
                ["bar","Bar"],
                ["btn","Button"],
                ["btnmatrix","Button_Matrix"],
 #                ["calendar","Calendar"],
#                ["calendar_header_arrow","Calendar_Header_Arrow"],
#                ["calendar_header_dropdown","Calendar_Header_Dropdown"],
                ["canvas","Canvas"],
                ["chart","Chart"],
                ["checkbox","Checkbox"],
                ["colorwheel","Colorwheel"],
                ["dropdown","Dropdown"],
                ["dropdownlist","Dropdown_List"],
#                ["imgbtn","Image_Button"],
                ["keyboard","Keyboard"],
                ["led","LED"],
                ["line","Line"],
                ["list","List"],
                ["list_text","List_Text"],
                ["list_btn","List_Button"],
#                ["menu","Menu"],
#                ["menu_page","Menu_Page"],
#                ["menu_cont","Menu_Content"],
#                ["menu_section","Menu_Section"],
#                ["menu_separator","Menu_Separator"],
#                ["menu_sidebar_cont","Menu_Sidebar_Content"],
#                ["menu_main_cont","Menu_Main_Content"],
#                ["menu_sidebar_header_cont","Menu_Sidebar_Header_Content"],
#                ["menu_main_header_cont","Menu_Main_Header_Content"],
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


    def __init__(self, Old_Name, Namespace):

        self.Old_Name = Old_Name
        self.Name = ""

        for O, N in Widget_Class.List:
            if O == Old_Name:
                self.Name = N

        # Delete file if it's exists
        Header_File_Path = os.path.join(Paths.Get_Bindings_Header_Path(), self.Name + ".hpp")
        if os.path.exists(Header_File_Path):
            os.remove(Header_File_Path)
        Source_File_Path = os.path.join(Paths.Get_Bindings_Source_Path(), self.Name + ".cpp")
        if os.path.exists(Source_File_Path):
            os.remove(Source_File_Path)

        self.Header_File = open(Header_File_Path, "w")
        self.Source_File = open(Source_File_Path, "w")
        # Check if file is open
        if not self.Header_File or not self.Source_File:
            raise print("Can't open file")


        self.Methods = []

        for Function in Namespace.free_functions():
            if Function.name.startswith("lv_" + self.Old_Name + "_"):
                self.Methods.append(Method.Method_Class(self, Function))
                
    def __del__(self):
        self.Header_File.close()
        self.Source_File.close()

    def Get_Old_Type_Name(self):
        return self.Old_Name

    def Get_Name(self):
        return self.Name

    def Get_Type_Name(self):
        return self.Name + "_Type"

    def Get_Class_Name(self):
        return self.Name + "_Class"

    def Write_Header_Header(self):
        self.Header_File.write("// Auto generated file\n\n")

        self.Header_File.write("#pragma once\n")
        self.Header_File.write("#include \"lvgl.h\"\n\n")

        if self.Name != "Object":
            self.Header_File.write("#include \"Object.hpp\"\n\n")
        
        self.Header_File.write("namespace LVGL\n")
        self.Header_File.write("{\n")
        self.Header_File.write("    typedef class " + self.Get_Class_Name())
    
        if self.Name != "Object":
            self.Header_File.write(" : public Object_Class")

        self.Header_File.write("\n\t{\n")
        self.Header_File.write("    public:\n")

    def Write_Header_Footer(self):
        self.Header_File.write("\n")

        # - Methods

        # - - Constructors

        if self.Get_Name() == "Object":
            self.Header_File.write("\t\tinline lv_obj_t* Get_LVGL_Pointer() const { return LVGL_Pointer; };\n")
            self.Header_File.write("\t\tinline void Clear_Pointer() { LVGL_Pointer = NULL; };\n")
            self.Header_File.write("\t\tinline " + self.Get_Class_Name() + "(lv_obj_t* LVGL_Pointer) : LVGL_Pointer(LVGL_Pointer) { };\n")
        
        else:
            self.Header_File.write("\t\tinline " + self.Get_Class_Name() + "(lv_obj_t* LVGL_Pointer) : Object_Class(LVGL_Pointer) { };\n")

        self.Header_File.write("\t\tinline " + self.Get_Class_Name() + "() = delete;\n")
        self.Header_File.write("\t\tinline " + self.Get_Class_Name() + "(" + self.Get_Class_Name() + "&& Object_To_Move) : Object_Class((lv_obj_t*)Object_To_Move) { Object_To_Move.Clear_Pointer(); }")
        # - - Operators
        self.Header_File.write("\t\tinline operator lv_obj_t*() const { return this->Get_LVGL_Pointer(); };\n\n")

        # - - Attributes

        self.Header_File.write("\t\tstatic const lv_obj_class_t& Class;\n")

        if self.Get_Name() == "Object":
            self.Header_File.write("\tprotected:\n")
            self.Header_File.write("\t\tlv_obj_t* LVGL_Pointer;\n")

        self.Header_File.write("    } " + self.Get_Type_Name() + ";\n")
        self.Header_File.write("}\n")

    def Write_Source_Header(self):
        self.Source_File.write("// Auto generated file\n\n")

        self.Source_File.write("#include \"" + self.Name + ".hpp\"\n\n")
        self.Source_File.write("using namespace LVGL;\n\n")

    def Write_Source_Footer(self):
        pass

    def Generate_Bindings(self):
        # - Header

        self.Write_Header_Header()

        # - - Methods

        for Method in self.Methods:
            self.Header_File.write("\t\t" + Method.Get_Prototype() + ";\n")

        
        self.Write_Header_Footer()

        # - Source

        self.Write_Source_Header()

        # - - Attributes

        self.Source_File.write(f"const lv_obj_class_t& {self.Get_Class_Name()}::Class = lv_{self.Get_Old_Type_Name()}_class;\n\n")

        # - - Methods

        for Method in self.Methods:
            self.Source_File.write(Method.Get_Definition() + "\n")

        self.Write_Source_Footer()

        #print ("=== Variables")
        #for Declaration in Global_Namespace.variables():
        #    if Basics.Get_Name(Declaration).startswith("lv_" + Widget_Name + "_"):
        #        print(Basics.Get_Name(Declaration))

    def Generate_All_Bindings(Namespace):
        for Widget_Old_Name, _ in Widget_Class.List:
            W = Widget_Class(Widget_Old_Name, Namespace)
            W.Generate_Bindings()
            #for Method in W.Methods:
                #print(f"{Method.Get_Old_Name()} -> {Method.Get_New_Name()}() : {Method.Get_Return_Type().Get_Converted_String()}")
                #print(f"{Method.Get_Prototype()}")
                #for A in Method.Get_Arguments():
                #    print(f"{A.Get_Name()} : {A.Get_Type().Get_Converted_String()}")
            
def Get_New_Widget_Name(Widget_Name):
    for Widget in Widgets_List:
        if Widget[0] == Widget_Name:
            return Widget[1]
    return None