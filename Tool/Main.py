import os
import shutil
import subprocess
from Basics import *
import Type

import Format
import Parse

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

import Documentation

import Log

import Main_Header

import Time

T = Time.Timer_Class()

# - Create generation folder

Paths.Create_Bindings_Folder(True)

# - Explore 

Method.Method_Class.Initialize()

Global_Namespace = Parse.Parse_LVGL()

if Global_Namespace is None:
    exit()

Log.Title("Generating bindings")

Widget.Widget_Class.Generate_All_Bindings(Global_Namespace)

Style.Style_Class(Global_Namespace).Generate_Bindings()

Color.Color_Class(Global_Namespace).Generate_Bindings()

Event.Event_Class(Global_Namespace).Generate_Bindings()

Group.Group_Class(Global_Namespace).Generate_Bindings()

Area.Area_Class(Global_Namespace).Generate_Bindings()

Timer.Timer_Class(Global_Namespace).Generate_Bindings()

Display.Display_Class(Global_Namespace).Generate_Bindings()

Main_Header.Generate()

Format.Format_Files()

Documentation.Generate()

Log.Title("[bold green]Bindings generated in " + T.Get_Time() + "[/bold green]")