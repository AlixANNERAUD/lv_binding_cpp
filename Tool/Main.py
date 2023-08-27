from pygccxml import utils
from pygccxml import declarations as Declarations
from pygccxml import parser as Parser

import os
import shutil
from Basics import *
import Type

import Widget
import Style
import Color

#import Widgets
import Paths
import Basics

# - PyGCCXML configuration

os.system("cls")

Generator_Path, Generator_Name = utils.find_xml_generator()

XML_Generator_Configuration = Parser.xml_generator_configuration_t(
    xml_generator_path=Generator_Path,
    xml_generator=Generator_Name)

# - Parse LVGL header

Decl = Parser.parse([Paths.Get_LVGL_Header_Path()], XML_Generator_Configuration)

# - Create generation folder

Paths.Create_Bindings_Folder(True)

# - Explore 

Global_Namespace = Declarations.get_global_namespace(Decl)

Widget.Widget_Class.Generate_All_Bindings(Global_Namespace)

Style.Style_Class(Global_Namespace).Generate_Bindings()

Color.Color_Class(Global_Namespace).Generate_Bindings()


#for Function in Global_Namespace.free_functions():
#    print(Function)

#    if (Get_Name(Function).startswith("lv_")):
#        print("---------------")

#        print(str(Function))
#        T = Type.Type_Class(Function.return_type)
#        print(T.Get_Informations(True))
        
        

        #T = Type.Type_Class(Function.return_type)
        #print(f"{type(T.Declaration)} {Get_Name(Function)} : {T.Get_String()} | P : {T.Is_Pointer()}")
        #if T.Is_Compound():
        #    print(f"P : {T.Get_Base().Is_Pointer()} | C : {T.Is_Constant()}")



# Widgets.Generate_All_Bindings(Declarations.get_global_namespace(Decl))


#print("=== Global var")

#for Declaration in Global_Namespace.variables():
#    if (Get_Name(Declaration).startswith("lv_")):
#        print(Get_Name(Declaration))

# print("=== Global const")

# for Declaration in Global_Namespace.declarations:
#     if (Get_Name(Declaration).startswith("LV_")):
#        print(Get_Name(Declaration))

# print("== Main header file")

Main_Header_File = Basics.Open_Main_Header_File()

Main_Header_File.write("#pragma once\n\n")

Main_Header_File.write("#include \"lvgl.h\"\n\n")

for _, Name in Widget.Widget_Class.List:
    Main_Header_File.write("#include \"" + Name + ".hpp\"\n")

Main_Header_File.close()