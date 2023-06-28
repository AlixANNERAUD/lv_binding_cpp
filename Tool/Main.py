from pygccxml import utils
from pygccxml import declarations as Declarations
from pygccxml import parser as Parser
import os
import shutil
from Basics import *
import Widgets
import Paths

# - PyGCCXML configuration

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

Widgets.Generate_All_Bindings(Declarations.get_global_namespace(Decl))


print("=== Global var")

for Declaration in Global_Namespace.variables():
    if (Get_Name(Declaration).startswith("lv_")):
        print(Get_Name(Declaration))

print("=== Global const")

for Declaration in Global_Namespace.declarations:
    if (Get_Name(Declaration).startswith("LV_")):
        print(Get_Name(Declaration))

