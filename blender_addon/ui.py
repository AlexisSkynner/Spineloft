import bpy
from . import gen_vol
from . import custom_editor
import time

######################### Operators ############################
class Operator_CreateVolume(bpy.types.Operator):
    bl_idname = "operator.createvolume"  # L'ID unique de l'opérateur
    bl_label = "Create volume"
    
    
    def execute(self, context):
        create_volume()
        return {'FINISHED'}
    

class Operator_DrawSpine(bpy.types.Operator):
    bl_idname = "operator.drawspine"  # L'ID unique de l'opérateur
    bl_label = "Draw spine"
    
         
    def invoke(self, context, event):
        custom_editor.createWindow()
        return {'RUNNING_MODAL'}
    

    
######################### Panels ############################   
class Panel_PhotoSketching(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "SpineLoft"
    bl_idname = "SPINELOFT_PT_PHOTOSKETCHING"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="SpineLoft", icon='CURVE_PATH')
        
        
        row = layout.row()
        row.operator(Operator_DrawSpine.bl_idname)

        row = layout.row()
        row.operator(Operator_CreateVolume.bl_idname)

    def execute(self, context):
        return {'FINISHED'}


######################### Functions ############################ 
def create_volume():
    
    #Création de la zone de data liée au volume
    crcl = bpy.data.meshes.new('circle')
    mesh=gen_vol.giveMeTheMesh()
    crcl.from_pydata(mesh[0],mesh[1],mesh[2])

    
    
    #Ajoute l'objet dans la collection actuelle 
    obj = bpy.data.objects.new('Circle', crcl)
    collection = bpy.context.collection
    collection.objects.link(obj)

def draw_spine():
    print("ok")
    

    