from pygccxml import utils
from pygccxml import declarations as Declarations
from pygccxml import parser as Parser

import Method

import Paths
import os

import Basics
import Base

class Style_Class(Base.Base_Class):


    def __init__(self, Namespace):
        Dependencies = ["Color"]

        Custom_Methods = [
            ("operator lv_style_t*()", "return &this->LVGL_Style;"),
        ]

        Base.Base_Class.__init__(self, "style", "Style", Namespace, "lv_style_t", "LVGL_Style", Dependencies=Dependencies, Custom_Methods=Custom_Methods)

    def Is_Method_Excluded(self, Method):
        if Method.name.startswith("lv_style_transition_dsc_init"):
            return True
        return False
    
    def Is_Constructor(self, Method_Name):
        return Method_Name.endswith("_init")

    def Is_Destructor(self, Method_Name):
        return Method_Name.endswith("_reset")
