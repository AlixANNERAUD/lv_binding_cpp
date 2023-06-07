import os

def Get_LVGL_Header_Path():
    return os.path.join(os.path.dirname(__file__), 'lvgl', 'lvgl.h')

def Get_lv_cpp_Path():
    return os.path.join(os.path.dirname(__file__), 'lv_cpp')

def Open_Widget_File(Widget, Header):
    if Header:
        return open(os.path.join(Get_lv_cpp_Path(), "lv_" + Widget[0] + ".h"), "w")

def Get_Name(Declaration):
    return Declaration.name