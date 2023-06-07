from pygccxml import utils
from pygccxml import declarations as Declarations
from pygccxml import parser as Parser
import os
from Basics import *
import Widgets

# - PyGCCXML configuration

Generator_Path, Generator_Name = utils.find_xml_generator()

XML_Generator_Configuration = Parser.xml_generator_configuration_t(
    xml_generator_path=Generator_Path,
    xml_generator=Generator_Name)

# - Parse LVGL header

Decl = Parser.parse([Get_LVGL_Header_Path()], XML_Generator_Configuration)

# - Explore 

Global_Namespace = Declarations.get_global_namespace(Decl)

print(type(Global_Namespace.declarations))

for Widget in Widgets.Widgets_List:
    print("== Widget", Widget[1], "==")

    print ("=== Functions")

    for Declaration in Global_Namespace.free_functions():
        if (Get_Name(Declaration).startswith("lv_" + Widget[0])):
            print(Get_Name(Declaration))


    print ("=== Variables")
    for Declaration in Global_Namespace.variables():
        if (Get_Name(Declaration).startswith("lv_" + Widget[0])):
            print(Get_Name(Declaration))

print("=== Global var")

for Declaration in Global_Namespace.variables():
    if (Get_Name(Declaration).startswith("lv_")):
        print(Get_Name(Declaration))

print("=== Global const")

for Declaration in Global_Namespace.declarations:
    if (Get_Name(Declaration).startswith("LV_")):
        print(Get_Name(Declaration))

