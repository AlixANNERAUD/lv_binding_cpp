import Basics
import Base

class Event_Class(Base.Base_Class):
    def __init__(self, Namespace):
        Base.Base_Class.__init__(self, "event", "Event", Namespace, "lv_event_t*", "LVGL_Event", Dependencies=["Object"])

    def Is_Method_Excluded(self, Method):
        return Method.name.startswith("lv_event_get_old_size") or Method.name.startswith("lv_event_get_cover_area")