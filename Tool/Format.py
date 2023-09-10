import subprocess

import Time
import Log
import Paths

def Format_Files():
    Log.Title("Formatting files")
    Log.Information("Formatting files...")

    Timer = Time.Timer_Class()
    
    Result = subprocess.run("cd " + Paths.Get_Bindings_Folder_Path() + " && clang-format -i src/*.cpp", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if Result.returncode != 0:
        Log.Error("Can't format source files : " + Result.stderr)
        return
    

    Result = subprocess.run("cd " + Paths.Get_Bindings_Folder_Path() + " && clang-format -i include/*.hpp", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if Result.returncode != 0:
        Log.Error("Can't format header files : " + Result.stderr)
        return

    Log.Success("Formatting files done in " + Timer.Get_Time())
