from pygccxml import utils
from pygccxml import declarations as Declarations
from pygccxml import parser as Parser

import Method

import Paths
import os

class Style_Class:
    def __init__(self, Namespace):
        self.Old_Name = "style"
        self.Name = "Style"

        Header_File_Path = os.path.join(Paths.Get_Bindings_Header_Path(), self.Name + ".hpp")
        if os.path.exists(Header_File_Path):
            os.remove(Header_File_Path)
        Source_File_Path = os.path.join(Paths.Get_Bindings_Source_Path(), self.Name + ".cpp")
        if os.path.exists(Source_File_Path):
            os.remove(Source_File_Path)

        self.Header_File = open(Header_File_Path, "w")
        self.Source_File = open(Source_File_Path, "w")

        self.Methods = []
       
        for Function in Namespace.free_functions():
            if Function.name.startswith("lv_" + self.Old_Name + "_"):
                self.Methods.append(Method.Method_Class(self, Function))


    def __del__(self):
        self.Header_File.close()
        self.Source_File.close()

    def Get_Old_Type_Name(self):
        return self.Old_Name


    def Get_Class_Name(self):
        return self.Name + "_Class"

    def Get_Type_Name(self):
        return self.Name + "_Type"

    def Write_Header_Header(self):
        self.Header_File.write("// Auto generated file\n\n")

        self.Header_File.write("#pragma once\n")
        self.Header_File.write("#include \"lvgl.h\"\n\n")

        self.Header_File.write("namespace LVGL\n")
        self.Header_File.write("{\n")
        self.Header_File.write("\ttypedef class " + self.Get_Class_Name())

        self.Header_File.write("\n\t{\n")
        self.Header_File.write("\tpublic:\n")
    
    def Write_Header_Footer(self):
        self.Header_File.write("\n")

        # - Methods

        # - - Operators

        self.Header_File.write("\t\tinline operator lv_style_t*() const { return &this->LVGL_Style; }\n")
        self.Header_File.write("\n")

        # - Attributes

        self.Header_File.write("\tprotected:\n\n")

        self.Header_File.write("\t\tlv_style_t LVGL_Style;\n")

        self.Header_File.write("\t} " + self.Get_Type_Name() + ";\n")
        self.Header_File.write("}\n")

    def Generate_Bindings(self):
        self.Write_Header_Header()

        for Method in self.Methods:
            self.Header_File.write("\t\t" + Method.Get_Prototype() + ";\n")

        self.Write_Header_Footer()

