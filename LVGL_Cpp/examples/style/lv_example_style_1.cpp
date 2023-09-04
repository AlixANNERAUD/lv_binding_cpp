#include "LVGL_Cpp.hpp"
#if LV_BUID_EXAMPLES && LV_USE_IMG

using namespace LVGL::Example;

void lv_example_style_1()
{
    static LVGL::Style_Type Style;
    Style.Set_Radius(5);

    /* Make a gradient */
    Style.Set_Width(150);
    Style.Set_Height(LV_SIZE_CONTENT);

    Style.Set_Pad_Ver(20);
    Style.Set_Pad_Left(5);

    Style.Set_X(lv_pct(50));
    Style.Set_Y(80);

    /* Create an object with the new style */

    LVGL::Object_Type Obj(LVGL::Object_Type::Get_Current_Screen());
    Obj.Add_Style(Style, 0);

    LVGL::Label_Type Label(Obj);
    Label.Set_Text("Hello");
}