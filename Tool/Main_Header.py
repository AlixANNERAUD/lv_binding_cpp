import Base

import Basics

import Log

def Generate():
    Log.Information("Generating main header file...")

    Main_Header_File = Basics.Open_Main_Header_File()

    Main_Header_File.write("#pragma once\n\n")
    Main_Header_File.write("#include \"lvgl.h\"\n\n")

    for Header_File in Base.Base_Class.Header_Files_List:
        Main_Header_File.write("#include \"" + Header_File + "\"\n")

    Main_Header_File.close()

    Log.Success("Main header file generated")


    