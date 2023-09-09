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
import Event
import Group
import Area
import Timer
import Display

import Method

#import Widgets
import Paths
import Basics

# - PyGCCXML configuration

if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

Generator_Path, Generator_Name = utils.find_xml_generator()

XML_Generator_Configuration = Parser.xml_generator_configuration_t(
    xml_generator_path=Generator_Path,
    xml_generator=Generator_Name)

# - Parse LVGL header

Decl = Parser.parse([Paths.Get_LVGL_Header_Path()], XML_Generator_Configuration)

# - Create generation folder

Paths.Create_Bindings_Folder(True)

# - Explore 

Method.Method_Class.Initialize_Header_Files_List()

Global_Namespace = Declarations.get_global_namespace(Decl)

Widget.Widget_Class.Generate_All_Bindings(Global_Namespace)

Style.Style_Class(Global_Namespace).Generate_Bindings()

Color.Color_Class(Global_Namespace).Generate_Bindings()

Event.Event_Class(Global_Namespace).Generate_Bindings()

Group.Group_Class(Global_Namespace).Generate_Bindings()

Area.Area_Class(Global_Namespace).Generate_Bindings()

Timer.Timer_Class(Global_Namespace).Generate_Bindings()

Display.Display_Class(Global_Namespace).Generate_Bindings()

Main_Header_File = Basics.Open_Main_Header_File()

Main_Header_File.write("#pragma once\n\n")

Main_Header_File.write("#include \"lvgl.h\"\n\n")

for _, Name in Widget.Widget_Class.List:
    Main_Header_File.write("#include \"" + Name + ".hpp\"\n")

Main_Header_File.write("#include \"Display.hpp\"")

Main_Header_File.close()

# Format using clang

print("clang-format -i " + Paths.Get_Bindings_Folder_Path() + "/*.hpp")

os.system("clang-format -i " + Paths.Get_Bindings_Folder_Path() + "/*.hpp")
os.system("clang-format -i " + Paths.Get_Bindings_Folder_Path() + "*.cpp")