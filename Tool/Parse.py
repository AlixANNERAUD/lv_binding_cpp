import Time

from pygccxml import utils
from pygccxml import declarations
from pygccxml import parser

import Paths
import Log

def Parse_LVGL():
    Log.Title("Parsing LVGL code")
    Log.Information("Parsing LVGL header file...")
    
    Timer = Time.Timer_Class()

    # - Try to find a C++ parser (XML generator)
    try:
        Generator_Path, Generator_Name = utils.find_xml_generator()
    except:
        Log.Error("Failed to find XML generator.")
        return None

    # - Configure the parser
    XML_Generator_Configuration = parser.xml_generator_configuration_t(
        xml_generator_path=Generator_Path,
        xml_generator=Generator_Name)

    # - Parse the LVGL header file
    try:
        Declarations = parser.parse([Paths.Get_LVGL_Header_Path()], XML_Generator_Configuration)
    except:
        Log.Error("Failed to parse LVGL header file.")
        return None

    Log.Success("Parsing LVGL code done in " + Timer.Get_Time())
    return declarations.get_global_namespace(Declarations)

    