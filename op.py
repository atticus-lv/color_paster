import bpy
from .utils import ColorPicker


class CP_OT_ColorPaster(bpy.types.Operator):
    bl_idname = "cp.color_paster"
    bl_label = "Paste Color"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.ops.ui.copy_data_path_button.poll()

    def execute(self, context):
        clipboard = context.window_manager.clipboard
        if not isinstance(clipboard, str): return {'CANCELLED'}
        clipboard.encode('utf8')

        CP = ColorPicker(clipboard)
        if not CP.bl_color: return {'CANCELLED'}

        print(CP.bl_color)
        # get property that need to paste
        bpy.ops.ui.copy_data_path_button(full_path=True)
        rna, prop = context.window_manager.clipboard.rsplit('.', 1)
        # some property only accept rgb values
        try:
            setattr(eval(rna), prop, CP.bl_color)
        except ValueError:
            setattr(eval(rna), prop, CP.bl_color[:3])
        # restore clip board
        context.window_manager.clipboard = clipboard

        return {'FINISHED'}





