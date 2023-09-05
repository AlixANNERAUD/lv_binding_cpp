from pygccxml import utils
from pygccxml import declarations as Declarations
from pygccxml import parser as Parser

import Basics
import Paths
import difflib

import os

import Method
import Type

import Base

# Currently ignoring widgets due to ambiguous naming
    



class Widget_Class(Base.Base_Class):

    List = [["obj","Object"],
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
                ["group", "Group"],
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

    def Is_Method_Excluded(self, Method):
        
        Best_Match = None
        Best_Match_Score = 0

        Splited_Method_Name = Method.name.replace("lv_", "").split("_")

        for Widget_Name, _ in Widget_Class.List:
            Current_Score = 0

            Splited_Widget_Name = Widget_Name.split("_")
            
            for i in range(min(len(Splited_Method_Name), len(Splited_Widget_Name))):
                if Splited_Method_Name[i] == Splited_Widget_Name[i]:
                    Current_Score += 1
                else:
                    break

            if Current_Score > Best_Match_Score:
                Best_Match = Widget_Name
                Best_Match_Score = Current_Score

        if Best_Match == None or self.Get_Old_Type_Name() != Best_Match or Method.name.startswith("lv_img_decoder"):        
            return True

        return False

    def __init__(self, Old_Name, Namespace):

        self.Old_Name = Old_Name
        self.Name = ""

        for O, N in Widget_Class.List:
            if O == Old_Name:
                self.Name = N

        Dependencies = None
        Heritage = None

        if self.Name == "Object":
            Dependencies = ["Style", "Area"]
        else:
            Heritage = "Object_Class"
            Dependencies = ["Object"]
    

        Base.Base_Class.__init__(self, Old_Name, self.Name, Namespace, "lv_obj_t*", "LVGL_Pointer", Dependencies=Dependencies, Heritage=Heritage)

    def __del__(self):
        Base.Base_Class.__del__(self)

    def Write_Header_Footer(self):
        self.Header_File.write("\n")

        # - Methods

        # - - Constructors

        if self.Get_Name() == "Object":
            self.Header_File.write("\t\tinline static Object_Class Get_Current_Screen() { return lv_scr_act(); };\n")
            self.Header_File.write("\t\tinline lv_obj_t* Get_LVGL_Pointer() const { return LVGL_Pointer; };\n")
            self.Header_File.write("\t\tinline void Clear_Pointer() { LVGL_Pointer = NULL; };\n")
            self.Header_File.write("\t\tinline " + self.Get_Class_Name() + "(lv_obj_t* LVGL_Pointer) : LVGL_Pointer(LVGL_Pointer) { };\n")
        else:
            self.Header_File.write("\t\tinline " + self.Get_Class_Name() + "(lv_obj_t* LVGL_Pointer) : Object_Class(LVGL_Pointer) { };\n")

        self.Header_File.write("\t\tinline " + self.Get_Class_Name() + "() = delete;\n")
        self.Header_File.write("\t\tinline " + self.Get_Class_Name() + "(" + self.Get_Class_Name() + "&& Object_To_Move) : Object_Class((lv_obj_t*)Object_To_Move) { Object_To_Move.Clear_Pointer(); }\n")
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
        Base.Base_Class.Write_Source_Header(self)

        # - - Attributes
        
        self.Source_File.write(f"const lv_obj_class_t& {self.Get_Class_Name()}::Class = lv_{self.Get_Old_Type_Name()}_class;\n\n")
        
    def Is_Constructor(self, Method_Name):
        return Method_Name.endswith("_create")

    def Is_Destructor(self, Method_Name):
        return Method_Name.endswith("_del")
            
    def Has_Method_This_Argument(self, Method):
        return Base.Base_Class.Has_Method_This_Argument(self, Method) and not(Method.Is_Constructor())

    def Generate_All_Bindings(Namespace):
        for Widget_Old_Name, _ in Widget_Class.List:
            W = Widget_Class(Widget_Old_Name, Namespace)
            W.Generate_Bindings()
