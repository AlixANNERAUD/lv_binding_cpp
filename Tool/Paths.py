import os
import shutil

def Find_File_By_Extension(Path, Extension):
    Files = []

    for Folder, Sub_Folders, Files_In_Folder in os.walk(Path):
        for File in Files_In_Folder:
            if File.endswith(Extension):
                Files.append(os.path.join(Folder, File))
    
    return Files

def Get_LVGL_Path():
    return os.path.join(os.path.dirname(__file__), '..', 'lvgl')

def Get_LVGL_Sources_Path():
    return os.path.join(Get_LVGL_Path(), 'src')

def Get_LVGL_Header_Path():
    return os.path.join(Get_LVGL_Path(), 'lvgl.h')

def Get_lv_cpp_Path():
    return os.path.join(os.path.dirname(__file__), '..', 'lv_cpp')

def Get_Bindings_Folder_Path():
    return os.path.join(os.path.dirname(__file__), '..', 'LVGL_Cpp')

def Get_Bindings_Header_Path():
    return os.path.join(Get_Bindings_Folder_Path(), 'include')

def Get_Bindings_Source_Path():
    return os.path.join(Get_Bindings_Folder_Path(), 'src')

def Create_Bindings_Folder(Remove_Existing_Folder = False):
    if Remove_Existing_Folder:
        if os.path.isdir(Get_Bindings_Header_Path()):
            shutil.rmtree(Get_Bindings_Header_Path())
        if os.path.isdir(Get_Bindings_Source_Path()):
            shutil.rmtree(Get_Bindings_Source_Path())

    os.mkdir(Get_Bindings_Header_Path())
    os.mkdir(Get_Bindings_Source_Path())
