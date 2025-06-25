import bpy
from . import gen_vol
from . import custom_editor
import time

    
class Operator_DrawSpine(bpy.types.Operator):
    bl_idname = "operator.drawspine"  # L'ID unique de l'opérateur
    bl_label = "Draw spine"
    
         
    def invoke(self, context, event):
        custom_editor.createWindow()
        return {'RUNNING_MODAL'}
    
    
######################### Panels ############################   
 
class Panel_SpineLoftOld(bpy.types.Panel):
    bl_label = "SpineLoftOld"
    bl_idname = "SPINELOFT_PT_SPINELOFTOLD"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="SpineLoft", icon='CURVE_PATH')
        
        
        row = layout.row()
        row.operator(Operator_DrawSpine.bl_idname)



    def execute(self, context):
        return {'FINISHED'}
   


