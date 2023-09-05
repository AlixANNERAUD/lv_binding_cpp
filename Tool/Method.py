from pygccxml import utils
from pygccxml import declarations
from pygccxml import parser as Parser

import re

import Widget
import Style
import Color
import Event
import Group
import Area
import Timer

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
        return self.Widget.Is_Constructor(self.Get_Old_Name())

    def Is_Destructor(self):
        return self.Widget.Is_Destructor(self.Get_Old_Name())


    def Get_Return_Type(self):
        return Type.Type_Class(self.Declaration.return_type)
        
    def Has_This_Argument(self):
        return self.Widget.Has_Method_This_Argument(self)

    def Get_Arguments(self):
        A = []
        
        for i, Argument in enumerate(self.Declaration.arguments):
            if not(i == 0 and self.Has_This_Argument()):
                A.append(Variable.Variable_Class(Type.Type_Class(Argument.decl_type), Argument.name))
        
        return A
        

    def Get_Prototype(self, For_Definition = False):
        D = ""

        if not(For_Definition):
            if self.Is_Constructor():
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

        for i, Argument in enumerate(self.Get_Arguments()):
            if i == 0 and self.Is_Constructor() and isinstance(self.Widget, Widget.Widget_Class):    # ! : Fix for invalid constructor issue
                D += "Object_Class& " + Argument.Get_New_Name() + ", " 
            else: 
                D += Argument.Get_Type().Get_Converted_String() + " " + Argument.Get_New_Name() + ", "

        if D.endswith(", "):
            D = D[:-2]

        return D + ")"
    

    def Get_Definition(self):

        D = self.Get_Prototype(True) + "\n{\n"

        if self.Is_Constructor():
            if self.Widget.Get_This_Attribute_Type().endswith("*"):
                if isinstance(self.Widget, Widget.Widget_Class):
                    D = D.replace("\n{\n", "")
                    D += " : Object_Class(NULL) \n{\n"
                D += "\t" + self.Widget.Get_This_Attribute_Name() + " = " + self.Get_Old_Name() + "("
            else:
                D += "\t" + self.Get_Old_Name() + "("
          
        elif self.Is_Destructor():
            D += "\t" + self.Get_Old_Name() + "("
        else:
            if self.Get_Return_Type().Is_Void():
                D += "\t" + self.Get_Old_Name() + "("
            else:
                D += "\treturn " + self.Get_Old_Name() + "("
        # Arguments

        if self.Has_This_Argument():
            D += self.Widget.Get_This_As_Argument() + ", "

        for Argument in self.Get_Arguments():
            D += Argument.Get_New_Name() + ", "

        while D.endswith(", "):
            D = D[:-2]

        D += ");\n"

        D += "}\n"

        return D
