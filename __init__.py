# SPDX-FileCopyrightText: 2020-2023 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This uses code from the Grease Pencil Tools addon included with blender by Samuel Bernou, Antonio Vazquez, Daniel Martinez Lara, Matias Mendiola
# Modified by William Spalding

bl_info = {
"name": "Brush Pack Importer",
"description": "Import brush packs from speciified .zip file",
"author": "",
"version": (1, 0, 0),
"blender": (3, 0, 0),
"location": "Sidebar > Grease Pencil > Grease Pencil Tools",
"warning": "",
"doc_url": "",
"tracker_url": "",
"category": "Object",
"support": "COMMUNITY",
}

import bpy
from .  import (import_brush_pack)

modules = (import_brush_pack)

def register():
    if bpy.app.background:
        return

    for mod in modules:
        mod.register()

def unregister():
    if bpy.app.background:
        return

    for mod in modules:
        mod.unregister()

if __name__ == "__main__":
    register()
