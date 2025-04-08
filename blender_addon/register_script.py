import bpy
from . import ui

# Initialisation
def register_all():
    bpy.utils.register_class(ui.Panel_PhotoSketching)
    bpy.utils.register_class(ui.Panel_Spinedrawer)
    bpy.utils.register_class(ui.Operator_CreateVolume)
    bpy.utils.register_class(ui.Operator_DrawSpine)
    


def unregister_all():
    bpy.utils.unregister_class(ui.Panel_PhotoSketching)
    bpy.utils.unregister_class(ui.Panel_Spinedrawer)
    bpy.utils.unregister_class(ui.Operator_CreateVolume)
    bpy.utils.unregister_class(ui.Operator_DrawSpine)

   