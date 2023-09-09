import Base

class Display_Class(Base.Base_Class):
    def __init__(self, Namespace):
        Base.Base_Class.__init__(self, "display", "Display", Namespace, "lv_disp_t*", "LVGL_Display")

    def __del__(self):
        Base.Base_Class.__del__(self)