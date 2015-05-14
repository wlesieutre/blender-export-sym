import bpy
from bpy_extras.io_utils import ExportHelper

bl_info = {
    "name":         "AGI32 SYM Format",
    "author":       "Will Lesieutre",
    "blender":      (2,74,0),
    "version":      (1,0,0),
    "location":     "File > Export",
    "description":  "Export AGI32 luminaire symbol",
    "category":     "Import-Export",
    "warning":      "Exports objects in local coordinates, apply transformations if needed"
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

        precision = 3 # Hardcoded decimal digits for now, TODO: add config parameter for rounding

        ob_verts_list = object.data.vertices

        for poly in object.data.polygons:
            poly_data = str(len(poly.vertices)) # First line of a polygon is the number of verts
            for vert_index in poly.vertices:
                vert_coords = object.data.vertices[vert_index].co
                print(vert_coords)
                vert_rounded = [round(vert_coords[0],precision), round(vert_coords[1],precision), round(vert_coords[2],precision)]
                # Append the vertex to poly_data
                poly_data += "\n" + str(vert_rounded[0]) + "  " + str(vert_rounded[1]) + "  " + str(vert_rounded[2])
                # TODO: Possible to convert a vector object with join?

            # Depending on the material channel assigned to the face, append poly_data to either 
            # the LUMINOUS or HOUSING section.
            # Increment the luminous and housing face counts, they're needed at the start of each section.
            if poly.material_index == 0:
                self.housing_count += 1
                self.housing_faces += "\n" + poly_data
            elif poly.material_index == 1:
                self.luminous_count += 1
                self.luminous_faces += "\n" + poly_data
            else:
                pass # TODO: Need to do anything with invalid material channels, or just drop the face?


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
