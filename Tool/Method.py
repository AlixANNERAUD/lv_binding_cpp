from pygccxml import utils
from pygccxml import declarations
from pygccxml import parser as Parser

import re
import Widget
import Style
import Color

import Type
import Variable

class Method_Class:
    def __init__(self, Widget, Declaration):
        self.Declaration = Declaration
        self.Widget = Widget

    def Get_Old_Name(self):
        return self.Declaration.name

    def Get_New_Name(self):
        if self.Is_Constructor():
            return self.Widget.Get_Class_Name()

        if self.Is_Destructor():
            return "~" + self.Widget.Get_Class_Name()

        New_Method_Name = self.Get_Old_Name().replace("lv_" + self.Widget.Get_Old_Type_Name() + "_", "")

        return re.sub(r"(^|_)([a-z])", lambda m: m.group(1) + m.group(2).upper(), New_Method_Name)

    def Is_Constructor(self):
        if isinstance(self.Widget, Widget.Widget_Class):
            return self.Get_Old_Name().endswith("_create")
        elif isinstance(self.Widget, Style.Style_Class):
            return self.Get_Old_Name().endswith("_init")

    def Is_Destructor(self):
        if isinstance(self.Widget, Widget.Widget_Class):
            return self.Get_Old_Name().endswith("_del")
        elif isinstance(self.Widget, Style.Style_Class):
            return self.Get_Old_Name().endswith("_reset")
    
    def Get_Return_Type(self):
        return Type.Type_Class(self.Declaration.return_type)
        
        D += ""
        if not(self.Widget.Is_Constructor or self.Widget.Is_Destructor()):
            #print(str(Declaration.return_type) + " : " + str(type(Declaration.return_type)))
            if self.Return_Type.Is_Pointer():
                Base = self.Return_Type.Get_Base()
                #print("base : ", str(Base))
                if Base.Is_Constant():
                    D += "const "
                    Base = Base.Get_Base()

                #print("base : ", str(type(Base)))

                if Base.Is_Declarated():
                    Declaration_String = Base.declaration.decl_string.replace("::", "").replace("lv_", "").replace("_t", "")
                    New_Type_Name = Get_New_Widget_Name(Declaration_String)
                    if New_Type_Name == None:
                        D += Base.decl_string + "* "
                    else:
                        D += New_Type_Name + "_Type "
                else:
                    D += Basics.Get_Type_Name(Base) + "* "
                    

                #D += Basics.Get_Type_Name(Base) + "* "

            else:
                D += Basics.Get_Type_Name(Declaration.return_type) + " " 

    def Has_This_Argument(self):
        if len(self.Declaration.arguments) == 0:
            return False

        First_Argument_Type = Type.Type_Class(self.Declaration.arguments[0].decl_type)

        if isinstance(self.Widget, Widget.Widget_Class):
            return "lv_obj_t*" in First_Argument_Type.Get_String().replace(" ", "").replace("const", "") and not(self.Is_Constructor())
        elif isinstance(self.Widget, Color.Color_Class):
            return "lv_color_t" in First_Argument_Type.Get_String().replace(" ", "").replace("const", "")
        elif isinstance(self.Widget, Style.Style_Class):
            return "lv_style_t*" in First_Argument_Type.Get_String().replace(" ", "").replace("const", "")

    def Get_Arguments(self):
        A = []
        
        for i, Argument in enumerate(self.Declaration.arguments):
            if not(i == 0 and self.Has_This_Argument()):
                A.append(Variable.Variable_Class(Type.Type_Class(Argument.decl_type), Argument.name))
        
        return A
        

    def Get_Prototype(self, For_Definition = False):
        D = ""

        if not(For_Definition):
            if self.Is_Constructor() and isinstance(self.Widget, Widget.Widget_Class):
                D += "explicit "
            elif self.Is_Destructor():
                D += "virtual "
            elif not(self.Has_This_Argument()):
                D += "static "

        if not(self.Is_Constructor()) and not(self.Is_Destructor()):
            D += self.Get_Return_Type().Get_Converted_String() + " "

        if For_Definition:
            D += self.Widget.Get_Class_Name() + "::" 
        
        D += self.Get_New_Name() + "("

        #if self.Is_Constructor():
        #    D += "Object_Class& Parent, "


        for i, Argument in enumerate(self.Get_Arguments()):
            if i == 0 and self.Is_Constructor():    # ! : Fix for invalid constructor issue
                D += "Object_Class& " + Argument.Get_New_Name() + ", " 
            else: 
                D += Argument.Get_Type().Get_Converted_String() + " " + Argument.Get_New_Name() + ", "

        if D.endswith(", "):
            D = D[:-2]

        return D + ")"
    

    def Get_Definition(self):

        D = self.Get_Prototype(True) + "\n{\n"

        if self.Is_Constructor() and isinstance(self.Widget, Widget.Widget_Class):
            D = D.replace("\n{\n", "")
            D += " : Object_Class(NULL) \n{\n"
            D += "\tLVGL_Pointer = " + self.Get_Old_Name() + "("
            
          
        elif self.Is_Destructor():
            D += "\t" + self.Get_Old_Name() + "("
        else:

            if self.Get_Return_Type().Is_Void():
                D += "\t" + self.Get_Old_Name() + "("
            else:
                D += "\treturn " + self.Get_Old_Name() + "("
        # Arguments

        if self.Has_This_Argument():
            if isinstance(self.Widget, Widget.Widget_Class):
                D += "LVGL_Pointer, "
            elif isinstance(self.Widget, Color.Color_Class):
                D += "LVGL_Color, "
            elif isinstance(self.Widget, Style.Style_Class):
                D += "&LVGL_Style, "

        for Argument in self.Get_Arguments():
            D += Argument.Get_New_Name() + ", "

        while D.endswith(", "):
            D = D[:-2]

        D += ");\n"

        D += "}\n"

        return D
