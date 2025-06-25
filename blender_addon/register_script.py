import bpy
from . import ui
from . import custom_editor
from . import tool

# Initialisation
def register_all():
    bpy.utils.register_class(ui.Panel_SpineLoftOld)
    bpy.utils.register_class(ui.Operator_DrawSpine)
    bpy.utils.register_class(custom_editor.Operator_UImanager)
    bpy.utils.register_class(custom_editor.Operator_SetBackgroundImage)
    tool.register()


def unregister_all():
    bpy.utils.unregister_class(ui.Panel_SpineLoftOld)
    bpy.utils.unregister_class(ui.Operator_DrawSpine)
    bpy.utils.unregister_class(custom_editor.Operator_UImanager)
    bpy.utils.unregister_class(custom_editor.Operator_SetBackgroundImage)
    tool.unregister()

   