import os
import shutil

def Get_LVGL_Header_Path():
    return os.path.join(os.path.dirname(__file__), '..', 'lvgl', 'lvgl.h')

def Get_lv_cpp_Path():
    return os.path.join(os.path.dirname(__file__), '..', 'lv_cpp')

def Get_Bindings_Folder_Path():
    return os.path.join(os.path.dirname(__file__), '..', 'Bindings')

def Get_Bindings_Header_Path():
    return os.path.join(Get_Bindings_Folder_Path(), 'include')

def Get_Bindings_Source_Path():
    return os.path.join(Get_Bindings_Folder_Path(), 'src')

def Create_Bindings_Folder(Remove_Existing_Folder = False):
    if Remove_Existing_Folder and os.path.isdir(Get_Bindings_Folder_Path()):
        shutil.rmtree(Get_Bindings_Folder_Path())



    os.mkdir(Get_Bindings_Folder_Path())

    os.mkdir(Get_Bindings_Header_Path())
    os.mkdir(Get_Bindings_Source_Path())
