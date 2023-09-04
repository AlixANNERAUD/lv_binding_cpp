import Basics
import Base

class Event_Class(Base.Base_Class):
    def __init__(self, Namespace):
        Base.Base_Class.__init__(self, "event", "Event", Namespace, Dependencies=["Object"])

    def __del__(self):
        Base.Base_Class.__del__(self)

    def Is_Method_Excluded(self, Method):
        return False

    def Write_Header_Footer(self):
        self.Header_File.write("\n")

        # - Methods

        # - - Operators

        self.Header_File.write("\t\tinline operator lv_event_t*() { return this->LVGL_Event; };\n")
        self.Header_File.write("\t\tinline Event_Class(lv_event_t* Event) : LVGL_Event(Event) { };\n")
        self.Header_File.write("\n")

        # - Attributes

        self.Header_File.write("\tprotected:\n")
        
        self.Header_File.write("\t\tlv_event_t* LVGL_Event;\n")

        self.Header_File.write("\t} Event_Type;\n")
        self.Header_File.write("}\n")
