bl_info = {
    "name": "Color Paster",
    "author": "Atticus",
    "version": (0.1),
    "blender": (2, 93, 0),
    "location": "F3 search(recommend to assign shortcut)",
    "description": "Paste the common color value with blender's style",
    # 'warning': "",
    # "doc_url": "",
    "category": "UI",
}

import bpy
from .op import CP_OT_ColorPaster


def register():
    bpy.utils.register_class(CP_OT_ColorPaster)


def unregister():
    bpy.utils.unregister_class(CP_OT_ColorPaster)


if __name__ == '__main__':
    register()
