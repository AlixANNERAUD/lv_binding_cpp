from pygccxml import declarations as Declarations
from pygccxml import parser as Parser
from pygccxml import utils

import os

import Basics
import Paths

import Method
import Type

class Color_Class:
    def __init__(self, Namespace):
        self.Old_Name = "color"
        self.Name = "Color"

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
            M = Method.Method_Class(self, Function)
            if M.Get_Old_Name().startswith("lv_" + self.Old_Name + "_"):
                if M.Get_Old_Name() != "lv_color_fill" and M.Get_Old_Name() != "lv_color_mix_with_alpha":  # ? : Remove this method due to issues with the arguments
                    self.Methods.append(M)
            
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

        # - - Palette

        self.Header_File.write("\t\tinline static Color_Class Get_Palette_Main(lv_palette_t p) { return lv_palette_main(p); };\n")
        self.Header_File.write("\t\tinline static Color_Class Get_Palette_Light(lv_palette_t p, uint8_t lvl) { return lv_palette_lighten(p, lvl); };\n")
        self.Header_File.write("\t\tinline static Color_Class Get_Palette_Dark(lv_palette_t p, uint8_t lvl) { return lv_palette_darken(p, lvl); };\n")
        self.Header_File.write("\n")

        # - - Operators

        self.Header_File.write("\t\tinline operator lv_color_t() { return this->LVGL_Color; };\n")
        self.Header_File.write("\t\tinline Color_Class(lv_color_t Color) { this->LVGL_Color = Color; };\n")
        self.Header_File.write("\n")

        # - Attributes

        self.Header_File.write("\tprotected:\n")
        
        self.Header_File.write("\t\tlv_color_t LVGL_Color;\n")

        self.Header_File.write("\t} Color_Type;\n")
        self.Header_File.write("}\n")

    def Write_Source_Header(self):
        self.Source_File.write("// Auto generated file\n\n")

        self.Source_File.write("#include \"" + self.Name + ".hpp\"\n\n")

        self.Source_File.write("using namespace LVGL;\n\n")

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
