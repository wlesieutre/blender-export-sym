import bpy
from bpy_extras.io_utils import ExportHelper

bl_info = {
    "name":         "AGI32 .sym exporter test",
    "author":       "Will Lesieutre",
    "blender":      (2,7,4),
    "version":      (0,0,1),
    "location":     "File > Import-Export",
    "description":  "Export AGI32 luminaire symbol",
    "category":     "Import-Export",
    "warning":      "In development, probably broken"
}

class ExportSYM(bpy.types.Operator, ExportHelper):
    bl_idname = "export_mesh.sym"
    bl_label = "Export SYM"
    bl_options = {'PRESET'}
    filename_ext = ".sym"


    def execute(self, context):
        print("Running execute")

def menu_export_func(self, context):
    self.layout.operator(ExportSYM.bl_idname, text="AGI32 Symbol (.sym)")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_export_func)
    print("Registering menu function")

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_export_func)
    print("Unregistering menu function")

if __name__ == "__main__":
    register()