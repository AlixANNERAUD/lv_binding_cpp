import Base

class Area_Class(Base.Base_Class):
    def __init__(self, Namespace):
        Base.Base_Class.__init__(self, "area", "Area", Namespace)

    def __del__(self):
        Base.Base_Class.__del__(self)
    
    def Is_Method_Excluded(self, Method):
        return False

    def Write_Header_Footer(self):
        self.Header_File.write("\n")

        # - Methods

        # - - Operators

        self.Header_File.write("\t\tinline operator const lv_area_t*() const { return &this->LVGL_Area; };\n")
        self.Header_File.write("\t\tinline operator lv_area_t*() { return &this->LVGL_Area; };\n")
        self.Header_File.write("\t\tinline Area_Class(const lv_area_t* Area) : Area_Class() { memcpy(&LVGL_Area, Area, sizeof(lv_area_t)); };\n")
        self.Header_File.write("\t\tinline Area_Class(lv_coord_t X1, lv_coord_t Y1, lv_coord_t X2, lv_coord_t Y2) : LVGL_Area{X1, Y1, X2, Y2} { };\n")
        self.Header_File.write("\t\tinline Area_Class() : LVGL_Area{0, 0, 0, 0} { };\n")

        self.Header_File.write("\n")

        # - Attributes

        self.Header_File.write("\tprotected:\n")

        self.Header_File.write("\t\tlv_area_t LVGL_Area;\n")

        self.Header_File.write("\t} Area_Type;\n")

        self.Header_File.write("}\n")