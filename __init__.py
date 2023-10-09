# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Hifumi will get the vertices and edges info from the grease pencil and export it as a file to be read by unreal engine

import bpy
from bpy.types import Context
from bpy.types import GPencilLayer
import os


bl_info = {
    "name" : "Hifumi",
    "author" : "smilecraft00",
    "description" : "Blender tool for goblin",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D > Sidebar > Hifumi",
    "warning" : "",
    "category" : "Import-Export"
}


# File format for the line art .gla (goblin line art)
# First line is the infor 

class HifumiPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Hifumi Panel"
    bl_idname = "OBJECT_PT_HifumiPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Hifumi'

    def draw(self, context: Context):
        layout = self.layout
        if SaveOperator.correct_type(context.active_object.type):
            layout = self.layout
            layout.prop(context.scene, "hifumi_save_path")
            layout.operator("hifumi.save_grease_pencil")

class SaveOperator(bpy.types.Operator):
    bl_idname = "hifumi.save_grease_pencil"
    bl_label = "Save Grease Pencil"

    def correct_type(object_type):
        if object_type == 'GPENCIL':
            return True
        
        return False
    
    def execute(self, context: Context):
        base_path, _ = os.path.splitext(context.scene.hifumi_save_path)
        file_path = base_path + ".hla"

        print(f"The file will be exported to {file_path}")

        gp_layer : GPencilLayer = context.active_gpencil_layer
        gp_strokes: bpy.types.GPencilStrokes = gp_layer.active_frame.strokes.values()

        try:
            with open(file_path, 'w') as file:
                file_version = "1.0.0"
                file_type = "hla"

                file.write("%s %s\n%s\n" % (file_type, file_version, len(gp_strokes)))

                for stroke in gp_strokes:
                    stroke: bpy.types.GPencilStroke
                    file.write("%s %s\n" % (len(stroke.points), stroke.line_width))
                    for point in stroke.points:
                        point: bpy.types.GPencilStrokePoint
                        file.write("%s %s %s %s %s %s %s %s %s\n" % (point.co.x, point.co.y, point.co.z, point.vertex_color[0], point.vertex_color[1], point.vertex_color[2], point.pressure, point.uv_factor, point.strength))
                    

        except Exception as e:
            print(f"Error writing to file {e}")

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(SaveOperator.bl_idname, text="Save Grease Pencil")


def register():
    bpy.types.Scene.hifumi_save_path = bpy.props.StringProperty(
        name='Save Path',
        subtype='FILE_PATH'
    )

    bpy.utils.register_class(HifumiPanel)
    bpy.utils.register_class(SaveOperator)
    # bpy.types.VIEW3D_MT_view.append(menu_func)

def unregister():
    bpy.utils.unregister_class(HifumiPanel)
    bpy.utils.unregister_class(SaveOperator)
    # bpy.types.VIEW3D_MT_view.remove(menu_func)
    del bpy.types.Scene.hifumi_save_path


if __name__ == "__main__":
    register()