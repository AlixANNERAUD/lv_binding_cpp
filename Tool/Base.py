import os

import Paths
import Method
import Basics

import Type


class Base_Class:

    Header_Files_List = []

    def __init__(self, Old_Name : str, New_Name : str, Namespace, This_Attribute_Type : str, This_Attribute_Name : str, Dependencies = None, Heritage = None, Custom_Methods = None, Custom_Attributes = None):
        self.Header_File_Scope = 0
        self.Source_File_Scope = 0
        
        self.Old_Name = Old_Name 
        self.Name = New_Name
        self.This_Attribute_Name = This_Attribute_Name
        self.This_Attribute_Type = This_Attribute_Type

        self.Custom_Methods = Custom_Methods
        self.Custom_Attributes = Custom_Attributes

        Header_File_Path = os.path.join(Paths.Get_Bindings_Header_Path(), self.Name + ".hpp")
        if os.path.exists(Header_File_Path):
            os.remove(Header_File_Path)
        Base_Class.Header_Files_List.append(self.Name + ".hpp")
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

    def Get_This_Name(self):
        return self.This_Attribute_Name

    def Get_This_Type(self):
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

    def Write_Line(self, File : str, Line : str = ""):
        self.Write(File, Line + "\n")

    def Write(self, File : str, String : str):
        if File[0] == 'H' or File[0] == 'h':
            self.Header_File.write(String)
        elif File[0] == 'S' or File[0] == 's':
            self.Source_File.write(String)

    def Increase_Scope(self, File : str, New_Line : bool = True):
        if New_Line:
            self.Write_Line(File, "{")
        else:
            self.Write(File, "{")

    def Decrease_Scope(self, File : str, New_Line : bool = True):
        if New_Line:
            self.Write_Line(File, "}")
        else:
            self.Write(File, "}")

    def Write_Header_Header(self):
        self.Write_Line('H', "// Auto generated file\n")

        self.Write_Line('H', "#pragma once")
        self.Write_Line('H', "#include \"lvgl.h\"")

        if self.Dependencies:
            for Dependency in self.Dependencies:
                self.Write_Line('H', "#include \"" + Dependency + ".hpp\"")

        self.Write_Line('H')

        self.Write_Line('H', f"namespace {Basics.Library_Namespace}")
        self.Increase_Scope('H')

        if self.Heritage:
            self.Write_Line('H', f"typedef class {self.Get_Class_Name()} : public {self.Heritage}")
        else:
            self.Write_Line('H', f"typedef class {self.Get_Class_Name()}")

        self.Increase_Scope('H')
        self.Write_Line('H', "public:")

    def Write_Header_Footer(self):

        # - Other methods
      
        # - - Custom

        if self.Get_This_Type().endswith("*") and not self.Heritage:
            self.Write_Line('H', "inline " + "void Clear_Pointer() { " + self.Get_This_Name() + " = NULL; };")

        if self.Custom_Methods:
            for Prototype, Definition in self.Custom_Methods:
                if Prototype.endswith("= delete"):
                    self.Write_Line('H', "inline " + Prototype + ";")
                else:    
                    self.Write_Line('H', "inline " + Prototype + " { " + Definition + " };")

        # - - Operators

        self.Write_Line('H', "inline operator " + self.Get_This_Type() + "() { return this->" + self.Get_This_Name() + "; };")
        self.Write_Line('H', "inline operator const " + self.Get_This_Type() + "() const { return this->" + self.Get_This_Name() + "; };")

        # - - Constructor

        if self.Heritage:
            self.Write_Line('H', "inline " + self.Get_Class_Name() + "(" + self.Get_This_Type() + " " + self.Get_This_Name() + ") : " + self.Heritage + "(" + self.Get_This_Name() + ") { };")
        else:
            self.Write_Line('H', "inline " + self.Get_Class_Name() + "(" + self.Get_This_Type() + " " + self.Get_This_Name() + ") : " + self.Get_This_Name() + "(" + self.Get_This_Name() + ") { };")

        # - - - Move

        if self.Get_This_Type().endswith("*"):
            if self.Heritage:
                self.Write_Line('H', "inline " + self.Get_Class_Name() + "(" + self.Get_Class_Name() + "&& Object_To_Move) : " + self.Heritage + "(Object_To_Move) { };")
            else:
                self.Write_Line('H', "inline " + self.Get_Class_Name() + "(" + self.Get_Class_Name() + "&& Object_To_Move) : " + self.Get_This_Name() + "(Object_To_Move." + self.Get_This_Name() + ") { Object_To_Move.Clear_Pointer(); };")



        # - Attributes

        if self.Custom_Attributes:
            for Custom_Attribute in self.Custom_Attributes:
                self.Write_Line('H', Custom_Attribute)

        if not self.Heritage:
            #self.Write_Line('H', "protected:")

            self.Write_Line('H', self.Get_This_Type() + " " + self.Get_This_Name() + ";")

        self.Write_Line('H', "}")

        self.Write_Line('H', self.Get_Type_Name() + ";")
        
        self.Write_Line('H', "}")



    def Write_Source_Header(self):
        self.Write_Line('S', "// Auto generated file\n")

        self.Write_Line('S', "#include \"" + self.Get_Name() + ".hpp\"")

        self.Write_Line('S', f"using namespace {Basics.Library_Namespace};\n")

    def Write_Source_Footer(self):
        pass

    def Generate_Bindings(self):
        self.Write_Header_Header()

        for M in self.Methods:
            self.Write_Line('H')
            self.Write_Line('H', M.Get_Documentation())
            self.Write_Line('H', M.Get_Prototype() + ";")

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
        if self.Get_This_Type().endswith("*"):
            return self.Get_This_Name()
        return "&" + self.Get_This_Name()

    def Has_Method_This_Argument(self, Method):
        if len(Method.Declaration.arguments) == 0:
            return False

        First_Argument_Type = Type.Type_Class(Method.Declaration.arguments[0].decl_type)

        return self.Get_This_Type() in First_Argument_Type.Get_String().replace(" ", "").replace("const", "")