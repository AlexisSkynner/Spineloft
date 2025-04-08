import bpy
from . import gen_vol

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
    
    text = bpy.props.StringProperty(name= "Enter Name", default= "")
    scale = bpy.props.FloatVectorProperty(name= "Scale:", default= (1,1,1))
    
    

    def execute(self, context):
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        area = bpy.context.window_manager.windows[-1].screen.areas[0]
        area.type = "IMAGE_EDITOR"
        area.header_text_set("Draw a spine")

        new_img = bpy.data.images.new(name="Test_Image", width=1024, height=1024)

        image_editor = area.spaces.active  
        image_editor.mode = 'PAINT'
        image_editor.image = bpy.data.images["Test_Image"]

        return {'FINISHED'}

    
######################### Panels ############################   
class Panel_PhotoSketching(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Photo Sketching"
    bl_idname = "panel.photosketching"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Super Spine Generator 2000", icon='CURVE_PATH')
        
        
        row = layout.row()
        row.operator(Operator_DrawSpine.bl_idname)

        row = layout.row()
        row.operator(Operator_CreateVolume.bl_idname)

    def execute(self, context):
        return {'FINISHED'}

class Panel_Spinedrawer(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Spine Drawer"
    bl_idname = "panel.spinedrawer"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Super Spine Generator 2000", icon='CURVE_PATH')
        
        
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
    

    