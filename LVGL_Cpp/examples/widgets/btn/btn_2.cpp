#include "../Examples.hpp"

#if LV_USE_BTN && LV_BUILD_EXAMPLES

using namespace LVGL::Examples;

void btn_2()
{
    static LVGL::Style_Type Style;
    
    Style.Set_Radius(3);

    Style.Set_Bg_Opa(LV_OPA_COVER);
    Style.Set_Bg_Color(LVGL::Color_Type::Get_Palette_Main(LV_PALETTE_BLUE));
    Style.Set_Bg_Grad_Color(LVGL::Color_Type::Get_Palette_Dark(LV_PALETTE_BLUE, 2));
    Style.Set_Bg_Grad_Dir(LV_GRAD_DIR_VER);

    Style.Set_Border_Opa(LV_OPA_40);
    Style.Set_Border_Width(2);
    Style.Set_Border_Color(LVGL::Color_Type::Get_Palette_Main(LV_PALETTE_GREY));

    Style.Set_Shadow_Width(8);
    Style.Set_Shadow_Color(LVGL::Color_Type::Get_Palette_Main(LV_PALETTE_GREY));
    Style.Set_Shadow_Ofs_Y(8);

    Style.Set_Outline_Opa(LV_OPA_COVER);
    Style.Set_Outline_Color(LVGL::Color_Type::Get_Palette_Main(LV_PALETTE_BLUE));
    
    Style.Set_Text_Color(LVGL::Color_Type::White());
    Style.Set_Pad_All(10);

    /*Init the pressed style*/
    static LVGL::Style_Type Style_Pr;

    /*Add a large outline when pressed*/
    Style_Pr.Set_Outline_Width(30);
    Style_Pr.Set_Outline_Opa(LV_OPA_TRANSP);
    Style_Pr.Set_Translate_Y(5);
    Style_Pr.Set_Shadow_Ofs_Y(3);
    Style_Pr.Set_Bg_Color(LVGL::Color_Type::Get_Palette_Dark(LV_PALETTE_BLUE, 2));
    Style_Pr.Set_Bg_Grad_Color(LVGL::Color_Type::Get_Palette_Dark(LV_PALETTE_BLUE, 4));

    /*Add a transition to the outline*/
    static lv_style_transition_dsc_t trans;
    static lv_style_prop_t props[] = {LV_STYLE_OUTLINE_WIDTH, LV_STYLE_OUTLINE_OPA, 0};
    lv_style_transition_dsc_init(&trans, props, lv_anim_path_linear, 300, 0, NULL);

    Style_Pr.Set_Transition(&trans);

    LVGL::Object_Type Btn1(LVGL::Object_Type::Get_Current_Screen());
    Btn1.Remove_Style_All();                          /*Remove the style coming from the theme*/
    Btn1.Add_Style(Style, 0);
    Btn1.Add_Style(Style_Pr, LV_STATE_PRESSED);
    Btn1.Set_Size(LV_SIZE_CONTENT, LV_SIZE_CONTENT);
    Btn1.Center();

    LVGL::Label_Type Label(Btn1);
    Label.Set_Text("Button");
    Label.Center();
}

#endif // LV_USE_BTN && LV_BUILD_EXAMPLES