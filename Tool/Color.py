from pygccxml import declarations as Declarations
from pygccxml import parser as Parser
from pygccxml import utils

import os

import Basics
import Paths

import Method
import Type
import Base

class Color_Class(Base.Base_Class):
    def __init__(self, Namespace):
        Custom_Methods = [
            ("static Color_Class Get_Palette_Main(lv_palette_t p)", "return lv_palette_main(p);"),
            ("static Color_Class Get_Palette_Light(lv_palette_t p, uint8_t lvl)", "return lv_palette_lighten(p, lvl);"),
            ("static Color_Class Get_Palette_Dark(lv_palette_t p, uint8_t lvl)", "return lv_palette_darken(p, lvl);"),

        ]

        Base.Base_Class.__init__(self, "color", "Color", Namespace, "lv_color_t", "LVGL_Color")
            
    def __del__(self):
        Base.Base_Class.__del__(self)

    def Is_Method_Excluded(self, Method):
        if Method.name.startswith("lv_color_mix_with_alpha") or Method.name.startswith("lv_color_fill"):
            return True
        return False
        
    def Get_This_As_Argument(self):
        return self.Get_This_Name()