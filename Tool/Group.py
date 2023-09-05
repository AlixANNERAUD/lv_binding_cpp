import Base

class Group_Class(Base.Base_Class):
    def __init__(self, Namespace):
        Base.Base_Class.__init__(self, "group", "Group", Namespace, "lv_group_t*", "LVGL_Group", Dependencies=["Object"])

    def __del__(self):
        Base.Base_Class.__del__(self)

    def Write_Header_Footer(self):
        self.Header_File.write("\n")

        # - Methods

        # - - Operators

        self.Header_File.write("\t\tinline operator lv_group_t*() { return this->LVGL_Group; };\n")
        self.Header_File.write("\t\tinline Group_Class(lv_group_t* Group) : LVGL_Group(Group) { };\n")
        self.Header_File.write("\n")

        # - Attributes

        self.Header_File.write("\tprotected:\n")
        
        self.Header_File.write("\t\tlv_group_t* LVGL_Group;\n")

        self.Header_File.write("\t} Group_Type;\n")
        self.Header_File.write("}\n")

    def Is_Constructor(self, Method_Name):
        return Method_Name.endswith("_create")

    def Is_Destructor(self, Method_Name):
        return Method_Name.endswith("_del")

