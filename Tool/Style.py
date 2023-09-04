from pygccxml import utils
from pygccxml import declarations as Declarations
from pygccxml import parser as Parser

import Method

import Paths
import os

import Basics
import Base

class Style_Class(Base.Base_Class):

    def Is_Method_Excluded(self, Method):
        if Method.name.startswith("lv_style_transition_dsc_init"):
            return True
        return False

    def __init__(self, Namespace):
        Dependencies = ["Color"]

        Base.Base_Class.__init__(self, "style", "Style", Namespace, Dependencies=Dependencies)

    def __del__(self):
        Base.Base_Class.__del__(self)
    
    def Write_Header_Footer(self):
        self.Header_File.write("\n")

        # - Methods

        # - - Operators

        self.Header_File.write("\t\tinline operator lv_style_t*() { return &this->LVGL_Style; };\n")
        self.Header_File.write("\n")

        # - Attributes

        self.Header_File.write("\tprotected:\n\n")

        self.Header_File.write("\t\tlv_style_t LVGL_Style;\n")

        self.Header_File.write("\t} " + self.Get_Type_Name() + ";\n")
        self.Header_File.write("}\n")


