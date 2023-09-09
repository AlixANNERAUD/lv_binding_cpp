import Base

class Area_Class(Base.Base_Class):
    def __init__(self, Namespace):

        Custom_Methods = [
            ("operator const lv_area_t*() const", "return &this->LVGL_Area;"),
            ("operator lv_area_t*()", "return &this->LVGL_Area;"),
            ("Area_Class(lv_coord_t X1, lv_coord_t Y1, lv_coord_t X2, lv_coord_t Y2) : LVGL_Area{X1, Y1, X2, Y2}", ""),
            ("Area_Class() : LVGL_Area{0, 0, 0, 0}", ""),
        ]

        Base.Base_Class.__init__(self, "area", "Area", Namespace, "lv_area_t", "LVGL_Area", Custom_Methods=Custom_Methods)