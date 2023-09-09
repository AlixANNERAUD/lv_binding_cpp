import Base

class Timer_Class(Base.Base_Class):
    def __init__(self, Namespace):
        Base.Base_Class.__init__(self, "timer", "Timer", Namespace, "lv_timer_t*", "LVGL_Timer")

    def __del__(self):
        Base.Base_Class.__del__(self)
        
    def Is_Constructor(self, Method_Name):
        return Method_Name.endswith("_create")

    def Is_Destructor(self, Method_Name):
        return Method_Name.endswith("_del")


