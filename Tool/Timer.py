import Base

class Timer_Class(Base.Base_Class):
    def __init__(self, Namespace):
        Base.Base_Class.__init__(self, "timer", "Timer", Namespace, "lv_timer_t*", "LVGL_Timer")

    def __del__(self):
        Base.Base_Class.__del__(self)

    def Write_Header_Footer(self):
        self.Header_File.write("\n")

        # - Methods

        # - - Operators

        self.Header_File.write("\t\tinline operator lv_timer_t*() { return this->LVGL_Timer; };\n")
        self.Header_File.write("\t\tinline Timer_Class(lv_timer_t* Timer) : LVGL_Timer(Timer) { };\n")
        self.Header_File.write("\n")

        # - Attributes

        self.Header_File.write("\tprotected:\n")
        
        self.Header_File.write("\t\tlv_timer_t* LVGL_Timer;\n")

        self.Header_File.write("\t} Timer_Type;\n")
        self.Header_File.write("}\n")

    def Is_Constructor(self, Method_Name):
        return Method_Name.endswith("_create")

    def Is_Destructor(self, Method_Name):
        return Method_Name.endswith("_del")


