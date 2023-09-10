import os
import subprocess

import Paths
import Base
import Log
import Time

# - Configuration

Enabled = True

# - Functions

def Generate():
    if not Enabled:
        return

    Log.Title("Generating documentation")

    Timer = Time.Timer_Class()

    Log.Information("Generating doxygen documentation...")
    
    Result = subprocess.run("cd " + os.path.join(Paths.Get_Bindings_Documentation_Path(), "Doxygen") + " && doxygen", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if Result.returncode != 0:
        Log.Error("Can't generate doxygen documentation : " + Result.stderr)
        return

    Log.Information("Generating sphinx documentation...")
    
    Result = subprocess.run("cd " + os.path.join(Paths.Get_Bindings_Documentation_Path(), "Sphinx") + " && make html", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if Result.returncode != 0:
        Log.Error("Can't generate sphinx documentation : " + Result.stderr)
        return

    Log.Success("Generating documentation done in " + Timer.Get_Time())



    
