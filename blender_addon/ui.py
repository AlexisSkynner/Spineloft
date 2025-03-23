import bpy
from . import gen_vol

#Partie UI
class Operator_CreateSpine(bpy.types.Operator):
    bl_idname = "operator.createspine"  # L'ID unique de l'opérateur
    bl_label = "Create"
    
    
    def execute(self, context):
        create_volume()
        return {'FINISHED'}
    
    
    

class Panel_PhotoSketching(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Photo Sketching"
    bl_idname = "panel.photosketching"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Super Spine Generator 2000", icon='CURVE_PATH')
        
        
        #row = layout.row()
        #row.operator("operator.showpicture")
        
        row = layout.row()
        row.operator("operator.createspine")
  
    

    def execute(self, context):
        return {'FINISHED'}




# Code

def create_volume():
    
    #Création de la zone de data liée au volume
    crcl = bpy.data.meshes.new('circle')
    mesh=gen_vol.giveMeTheMesh()
    crcl.from_pydata(mesh[0],mesh[1],mesh[2])

    
    
    #Ajoute l'objet dans la collection actuelle 
    obj = bpy.data.objects.new('Circle', crcl)
    collection = bpy.context.collection
    collection.objects.link(obj)