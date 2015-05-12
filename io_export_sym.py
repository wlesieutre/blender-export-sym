import bpy
from bpy_extras.io_utils import ExportHelper

bl_info = {
    "name":         "AGI32 .sym exporter test",
    "author":       "Will Lesieutre",
    "blender":      (2,7,4),
    "version":      (0,0,2),
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

        if self.filepath == "":
            print("Error: Filepath not specified") # TODO: Need to give error message to blender?
            return {'FINISHED'}

        objects_to_export = [object for object in bpy.context.selected_objects if object.type == "MESH"]

        self.header = "ENTITY " + self.filepath + "\n" # TODO: isolate file name, instead of full path
        self.luminous = "LUMINOUS\n"
        self.luminous_count = 0
        self.luminous_faces = ""
        self.housing = "\nHOUSING\n"
        self.housing_count = 0
        self.housing_faces = ""
        self.footer = "\nEND ENTITY"
        self.exported_count = 0

        # Export each object. Currently uses all selected objects, TODO: add "Export Selected" like some other exporters?
        for object in objects_to_export:
            self.exported_count += 1
            self.export_object(object)

        # Concatenate data and write to file
        self.luminous += str(self.luminous_count) + self.luminous_faces
        self.housing += str(self.housing_count) + self.housing_faces
        file_text = self.header + self.luminous + self.housing + self.footer

        file = open(self.filepath, "w")
        file.write(file_text)
        file.close()

        return {'FINISHED'}

    def export_object(self, object):

        # TODO: Iterate through objects's polygons/vertices and create face data
        #       for luminous_faces and housing_faces. Track face counts for each.

        pass


def menu_export_func(self, context):
    self.layout.operator(ExportSYM.bl_idname, text="AGI32 Symbol (.sym)")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_export_func)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_export_func)

if __name__ == "__main__":
    register()
