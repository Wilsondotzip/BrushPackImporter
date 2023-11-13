# SPDX-FileCopyrightText: 2020-2023 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This uses code from the Grease Pencil Tools addon included with blender by Samuel Bernou, Antonio Vazquez, Daniel Martinez Lara, Matias Mendiola. Grease Pencil Tools addon is published on GitHub by 'Pullusb' https://github.com/Pullusb/greasepencil-addon/tree/master
# 
# This addon Brush Pack Importer is created by William Spalding (Wilson Digital Design)

import bpy
from cProfile import label
import bpy
import zipfile
from pathlib import Path

from bpy.props import (StringProperty,
                       PointerProperty,
                       )

from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

def unzip(zip_path, extract_dir_path):
    '''Get a zip path and a directory path to extract to'''
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir_path)

def get_brushes(blend_fp):
    cur_brushes = [b.name for b in bpy.data.brushes]
    with bpy.data.libraries.load(str(blend_fp), link=False) as (data_from, data_to):
        # load brushes starting     with 'tex' prefix if there are not already there
        data_to.brushes = [b for b in data_from.brushes if not b in cur_brushes]
        data_to.materials = [m for m in data_from.materials if m]
        # Add holdout
        if 'z_holdout' in data_from.brushes and not 'z_holdout' in cur_brushes:
            data_to.brushes.append('z_holdout')

    ## force fake user for the brushes
    for b in data_to.brushes:
        b.use_fake_user = True

    return len(data_to.brushes)

class ImportProperties(bpy.types.PropertyGroup):
    my_label : bpy.props.StringProperty(name= "")
    path : StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')
    
class BRUSHPACKIMPORTER_PT_main_panel(bpy.types.Panel):
    bl_label = "Import Brushes"
    bl_idname = "ADDONNAME_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Import Brushes"

    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        col = layout.column(align=True)
        col.prop(scene.my_tool, "path", text="")
        layout.operator("addonname.myop_operator")
        




class BRUSHPACKIMPORTER_OT_my_op(bpy.types.Operator):
    
    bl_label = "Import"
    bl_idname = "addonname.myop_operator"
    brushzip: bpy.props.StringProperty(subtype='FILE_PATH')
    directory: StringProperty(
        name="Outdir Path",
        description="Import dir"
        )
    
    
    
    def _append_brushes(self, blend_fp):
        cur_brushes_before = [b.name for b in bpy.data.brushes]
        get_brushes(blend_fp)
        cur_brushes_after = [b.name for b in bpy.data.brushes]

        brushes_added = set(cur_brushes_after) - set(cur_brushes_before)

        if brushes_added:
            added_brush_count = len(brushes_added)
            self.report({'INFO'}, f'{added_brush_count} brushes installed: {", ".join(brushes_added)}')
        else:
            self.report({'WARNING'}, 'Brushes already loaded')

    def _install_from_zip(self):
        ## get blend file name
        blendname = None
        with zipfile.ZipFile(self.brushzip, 'r') as zfd:
            for f in zfd.namelist():
                if f.endswith('.blend'):
                    blendname = f
                    break
        if not blendname:
            self.report({'ERROR'}, f'blend file not found in zip {self.brushzip}')
            return

        unzip(self.brushzip, self.temp)

        self._append_brushes(Path(self.temp) / blendname)

    def execute(self, context):
        import tempfile
        import os
        scene = context.scene
        mytool = scene.my_tool
        
        self.brushzip = mytool.path
        temp = tempfile.gettempdir()
        self.temp = Path(temp)
        #self.brushzip = "custom path for debug"
              
        print("Selected Directory:") 
        self._install_from_zip()
        return {"FINISHED"}










classes = [ImportProperties, BRUSHPACKIMPORTER_PT_main_panel, BRUSHPACKIMPORTER_OT_my_op]
 
 
 
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
        bpy.types.Scene.my_tool = bpy.props.PointerProperty(type= ImportProperties)
 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.my_tool
 
 
 
if __name__ == "__main__":
    register()
