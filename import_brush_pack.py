# SPDX-FileCopyrightText: 2020-2023 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This uses code from the Grease Pencil Tools addon included with blender by Samuel Bernou, Antonio Vazquez, Daniel Martinez Lara, Matias Mendiola
# Modified by William Spalding

import bpy
import zipfile
from pathlib import Path

def unzip(zip_path, extract_dir_path):
    '''Get a zip path and a directory path to extract to'''
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir_path)

def get_brushes(blend_fp):
    cur_brushes = [b.name for b in bpy.data.brushes]
    with bpy.data.libraries.load(str(blend_fp), link=False) as (data_from, data_to):
        # load brushes starting with 'tex' prefix if there are not already there
        data_to.brushes = [b for b in data_from.brushes if b.startswith('P') and not b in cur_brushes]
        data_to.materials = [m for m in data_from.materials if m]
        # Add holdout
        if 'z_holdout' in data_from.brushes and not 'z_holdout' in cur_brushes:
            data_to.brushes.append('z_holdout')

    ## force fake user for the brushes
    for b in data_to.brushes:
        b.use_fake_user = True

    return len(data_to.brushes)

class GP_OT_install_brush_pack(bpy.types.Operator):
    bl_idname = "gp.import_brush_pack"
    bl_label = "Download and import texture brush pack"
    bl_description = "Import Grease Pencil brush pack from a local .zip archive"
    bl_options = {"REGISTER", "INTERNAL"}


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
        temp = tempfile.gettempdir()
        self.temp = Path(temp)
        self.brushzip = "C:\\Users\\wspal\\AppData\\Roaming\\Blender Foundation\\Blender\\3.6\\scripts\\B4C_PencilBrushes_v2.zip"
        print(f'{self.brushzip} is up do date, appending brushes')
        self._install_from_zip()
        return {"FINISHED"}

        


def register():
    bpy.utils.register_class(GP_OT_install_brush_pack)

def unregister():
    bpy.utils.unregister_class(GP_OT_install_brush_pack)
