import os

import Paths
import Method
import Basics

import Type


class Base_Class:

    def __init__(self, Old_Name : str, New_Name : str, Namespace, This_Attribute_Type : str, This_Attribute_Name : str, Dependencies = None, Heritage = None, Custom_Method = None):
        self.Header_File_Scope = 0
        self.Source_File_Scope = 0
        
        self.Old_Name = Old_Name 
        self.Name = New_Name
        self.This_Attribute_Name = This_Attribute_Name
        self.This_Attribute_Type = This_Attribute_Type

        Header_File_Path = os.path.join(Paths.Get_Bindings_Header_Path(), self.Name + ".hpp")
        if os.path.exists(Header_File_Path):
            os.remove(Header_File_Path)
        Source_File_Path = os.path.join(Paths.Get_Bindings_Source_Path(), self.Name + ".cpp")
        if os.path.exists(Source_File_Path):
            os.remove(Source_File_Path)

        self.Header_File = open(Header_File_Path, "w")
        self.Source_File = open(Source_File_Path, "w")

        if not self.Header_File or not self.Source_File:
            raise print(f"Can't open file {self.Name}")

        self.Methods = []

        for Function in Namespace.free_functions():
            if Function.name.startswith("lv_" + self.Old_Name + "_"):
                if not self.Is_Method_Excluded(Function):
                    self.Methods.append(Method.Method_Class(self, Function))

        self.Dependencies = Dependencies
        self.Heritage = Heritage

    def __del__(self):
        self.Header_File.close()
        self.Source_File.close()

    def Get_This_Attribute_Name(self):
        return self.This_Attribute_Name

    def Get_This_Attribute_Type(self):
        return self.This_Attribute_Type

    def Is_Method_Excluded(self, Method):
        return False

    def Get_Old_Type_Name(self):
        return self.Old_Name

    def Get_Name(self):
        return self.Name

    def Get_Class_Name(self):
        return self.Name + "_Class"

    def Get_Type_Name(self):
        return self.Name + "_Type"

    def Add_Line(self, File : str, Line : str):
        if File[0] == 'H' or File[0] == 'h':
            for i in range(self.Header_File_Scope):
                Line = "\t" + Line
            self.Header_File.write(Line + "\n")
        elif File[0] == 'S' or File[0] == 's':
            for i in range(self.Source_File_Scope):
                Line = "\t" + Line
            self.Source_File.write(Line + "\n")

    def Increase_Scope(self, File : str):
        if File[0] == 'H' or File[0] == 'h':
            self.Add_Line('H', "{")
            self.Header_File_Scope += 1
        elif File[0] == 'S' or File[0] == 's':
            self.Add_Line('S', "{")
            self.Source_File_Scope += 1

    def Decrease_Scope(self, File : str):
        if File[0] == 'H' or File[0] == 'h':
            self.Add_Line('H', "}")
            self.Header_File_Scope -= 1
        elif File[0] == 'S' or File[0] == 's':
            self.Add_Line('S', "}")
            self.Source_File_Scope -= 1    

    def Write_Header_Header(self):
        self.Header_File.write("// Auto generated file\n\n")

        self.Add_Line('H', "#pragma once")
        self.Add_Line('H', "#include \"lvgl.h\"")

        for Dependency in self.Dependencies:
            self.Add_Line('H', "#include \"" + Dependency + ".hpp\"")

        self.Add_Line('H', f"namespace {Basics.Library_Namespace}")
        
        self.Increase_Scope('H')
        self.Add_Line('H', f"typedef class {self.Get_Class_Name()}")
        if self.Heritage:
            self.Add_Line('H', f" : public {self.Heritage}")
        self.Add_Line('H', "{")
        
        self.Increase_Scope('H')
        self.Add_Line('H', "public:")

    def Write_Source_Header(self):
        self.Add_Line('S', "// Auto generated file\n")

        self.Add_Line('S', "#include \"" + self.Get_Name() + ".hpp\"")

        self.Add_Line('S', f"using namespace {Basics.Library_Namespace};\n")

    def Write_Source_Footer(self):
        pass

    def Generate_Bindings(self):
        self.Write_Header_Header()

        for M in self.Methods:
            self.Header_File.write("\t\t" + M.Get_Prototype() + ";\n")

        self.Write_Header_Footer()

        self.Write_Source_Header()

        for M in self.Methods:
            self.Source_File.write(M.Get_Definition() + "\n")

        self.Write_Source_Footer()

    def Is_Constructor(self, Method_Name : str):
        return False

    def Is_Destructor(self, Method_Name : str):
        return False
            
    def Get_This_As_Argument(self):
        if self.Get_This_Attribute_Type().endswith("*"):
            return self.Get_This_Attribute_Name()
        return "&" + self.Get_This_Attribute_Name()

    def Has_Method_This_Argument(self, Method):
        if len(Method.Declaration.arguments) == 0:
            return False

        First_Argument_Type = Type.Type_Class(Method.Declaration.arguments[0].decl_type)

        return self.Get_This_Attribute_Type() in First_Argument_Type.Get_String().replace(" ", "").replace("const", "")

        