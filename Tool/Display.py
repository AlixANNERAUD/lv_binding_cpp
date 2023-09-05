import Base

class Display_Class(Base.Base_Class):
    def __init__(self, Namespace):
        Base.Base_Class.__init__(self, "display", "Display", Namespace, "lv_disp_t*", "LVGL_Display")

    def __del__(self):
        Base.Base_Class.__del__(self)

    def Is_Method_Excluded(self, Method):
        return False

    def Write_Header_Footer(self):
        self.Header_File.write("\n")

        # - Methods

        # - - Operators

        self.Header_File.write("\t\tinline operator lv_disp_t*() { return this->LVGL_Display; };\n")
        self.Header_File.write("\t\tinline Display_Class(lv_disp_t* Display) : LVGL_Display(Display) { };\n")
        self.Header_File.write("\n")

        # - Attributes

        self.Header_File.write("\tprotected:\n")
        
        self.Header_File.write("\t\tlv_disp_t* LVGL_Display;\n")

        self.Header_File.write("\t} Display_Type;\n")
        self.Header_File.write("}\n")