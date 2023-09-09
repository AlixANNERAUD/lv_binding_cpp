import Basics
import Base

class Event_Class(Base.Base_Class):
    def __init__(self, Namespace):

        Base.Base_Class.__init__(self, "event", "Event", Namespace, "lv_event_t*", "LVGL_Event", Dependencies=["Object"])

    def __del__(self):
        Base.Base_Class.__del__(self)