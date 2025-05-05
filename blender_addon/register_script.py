import bpy
from . import ui
from . import custom_editor

# Initialisation
def register_all():
    bpy.utils.register_class(ui.Panel_PhotoSketching)
    bpy.utils.register_class(ui.Panel_Spinedrawer)
    bpy.utils.register_class(ui.Operator_CreateVolume)
    bpy.utils.register_class(ui.Operator_DrawSpine)
    bpy.utils.register_class(custom_editor.Operator_UImanager)
    bpy.utils.register_class(custom_editor.Operator_SetBackgroundImage)


def unregister_all():
    bpy.utils.unregister_class(ui.Panel_PhotoSketching)
    bpy.utils.unregister_class(ui.Panel_Spinedrawer)
    bpy.utils.unregister_class(ui.Operator_CreateVolume)
    bpy.utils.unregister_class(ui.Operator_DrawSpine)
    bpy.utils.unregister_class(custom_editor.Operator_UImanager)
    bpy.utils.unregister_class(custom_editor.Operator_SetBackgroundImage)

   