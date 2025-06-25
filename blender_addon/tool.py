import bpy
from bl_ui.space_toolsystem_common import ToolDef
import mathutils
import math
from bpy_extras import view3d_utils
from . import intersect
from . import gen_vol
from . import d2

path = None
spline = None
list_points = []

curve_data = None
curve_obj=None
spline = None
drawing_mode="None"
step=0

image_width=0
image_height=0

# Opérateur simple que notre outil lancera
class Operator_Select_Image(bpy.types.Operator):
    """Select a reference picture, that will be used to generate your 3D model. For more informations, check the documentation."""
    bl_idname = "wm.select_image"
    bl_label = "File browser"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        global path
        global step
        global image_width
        global image_height
        global pixels
        try :
            image = bpy.data.images.load(self.filepath)
            path=str(self.filepath)
            pixels=[p for p in image.pixels]
            
            size=image.size
            image_height=size[1]
            image_width=size[0]

            
            
            move_view3d_to((0,0,-1),(0,0,0))
            bpy.ops.view3d.view_axis(type='TOP')
            create_ref_image(path)
            step=1
        except:
            path=None
        return {'FINISHED'}

    def invoke(self, context, event):
        
        context.window_manager.fileselect_add(self)  # ouvre la fenêtre de fichier
        return {'RUNNING_MODAL'}


class Operator_Draw_FH(bpy.types.Operator):
    """Draw the spine freehand."""
    bl_idname = "wm.draw_freehand"
    bl_label = "Draw - Freehand"
    holding=False

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            # Récupérer la position du rayon (origine + direction)
            self.holding=True            



        if event.type in {'ESC','RIGHTMOUSE', 'MIDDLEMOUSE'} or (event.type == 'LEFTMOUSE' and event.value == 'RELEASE'):
            global drawing_mode
            global step
            self.holding=False
            drawing_mode = "None"
            bpy.context.area.tag_redraw()
            step=2
            return {'FINISHED'}
        
        if event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}

        if self.holding==True:
            pos = get_mouse_3d_location(context, event)
            self.report({'INFO'}, f"Clic en {pos[0]}, {pos[1]}")
            add_stroke_point(pos)


        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        global path
        global drawing_mode
        global step
        step=1
        drawing_mode = "Freehand"
        move_view3d_to((0,0,-1),(0,0,0))
        bpy.ops.view3d.view_axis(type='TOP')
        create_curve()

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class Operator_Draw_SL(bpy.types.Operator):
    """Draw the spine with straight lines."""
    bl_idname = "wm.draw_straight_lines"
    bl_label = "Draw - Straight lines"
    

    def modal(self, context, event):
        global drawing_mode
        global step

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            
            pos = get_mouse_3d_location(context, event)
            
            if pos[0]<=0.5 and pos[1]<=0.5 and pos[0]>=-0.5 and pos[1]>=-0.5:
                add_stroke_point(pos) 
            
            else:
                drawing_mode = "None"
                bpy.context.area.tag_redraw()
                step=2
                return {'FINISHED'}

                             

        if event.type in {'ESC','RIGHTMOUSE', 'MIDDLEMOUSE'}:
            drawing_mode = "None"
            bpy.context.area.tag_redraw()
            step=2
            return {'FINISHED'}
        
        if event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        global path
        global drawing_mode
        global step
        step=1
        drawing_mode = "Straight Lines"
        move_view3d_to((0,0,-1),(0,0,0))
        bpy.ops.view3d.view_axis(type='TOP')
        create_curve()

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class Operator_Clear_Spine(bpy.types.Operator):
    """Clear the spine."""
    bl_idname = "wm.clear_spine"
    bl_label = "Clear"
    
    def invoke(self, context, event):
        global step
        step=1
        delete_curve()
        return {'FINISHED'}

class Operator_Generate_Volume(bpy.types.Operator):
    """Generate your 3D volume."""
    bl_idname = "wm.gen_vol"
    bl_label = "Generate 3D Volume"
    
    def invoke(self, context, event):
        ratio_x = min(1, image_width / image_height)
        ratio_y = min(1, image_height / image_width)

        image_dest=[0]*image_height*image_width
        for i in range(0,image_width*image_height*4,4):
            r = pixels[i]
            g = pixels[i+1]
            b = pixels[i+2]
            image_dest[i//4]=int((r*0.2989+g*0.587+b*0.114)*255)


        new_stroke = redistribute_stroke(list_points)
        list_points_denormalized=[((p[0]+0.5) * ratio_x * image_width, (0.5 - p[1]) * ratio_y * image_height) for p in new_stroke]
    
        ribs = intersect.intersect(image_width, image_height, image_dest, list_points_denormalized, [], 1)

        edges_list = []
        for i in range(len(ribs)):
            # a verifier le [i][0][0] pour le format de retour de intersect
            x1 = ribs[i][0][0]
            y1 = ribs[i][0][1]

            x2 = ribs[i][1][0]
            y2 = ribs[i][1][1]

            xd1 = (x1 / image_width - 0.5)   * ratio_x
            yd1 = -(y1 / image_height - 0.5) * ratio_y
            xd2 = (x2 / image_width - 0.5)   * ratio_x
            yd2 = -(y2 / image_height - 0.5) * ratio_y

            edges_list.append((x1, y1, 0))
            edges_list.append((x2, y2, 0))

        

        #Création de la zone de data liée au volume
        crcl = bpy.data.meshes.new('circle')
        mesh=gen_vol.giveMeTheMesh(edges_list)
        crcl.from_pydata(mesh[0],mesh[1],mesh[2])
        
        #Ajoute l'objet dans la collection actuelle 
        obj = bpy.data.objects.new('Circle', crcl)
        bpy.context.window.scene.collection.objects.link(obj)
        return {'FINISHED'}

class Panel_SpineLoft(bpy.types.Panel):
    bl_label = "SpineLoft tool"
    bl_idname = "SPINELOFT_PT_SPINELOFT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category="Tool"
    
    def draw(self, context):
        layout = self.layout

class Panel_Select_Image(bpy.types.Panel):
    bl_label = "Reference Selector (Step 1)"
    bl_idname = "SPINELOFT_PT_SELECTIMAGE"
    bl_parent_id = "SPINELOFT_PT_SPINELOFT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category="Tool"
    


    def draw(self, context):
        layout = self.layout
        layout.label(text="Select the reference image to use.")
        
        row = layout.row(align=True)
        showed_path=path+"\n\n" if path else " Open a file"
        row.operator("wm.select_image", text=showed_path, icon="FILE_FOLDER")


class Panel_Draw_Tools(bpy.types.Panel):
    bl_label = "Drawing Tools (Step 2)"
    bl_idname = "SPINELOFT_PT_DRAWTOOLS"
    bl_parent_id = "SPINELOFT_PT_SPINELOFT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category="Tool"
    
    @classmethod
    def poll(cls, context):
        if step==0:
            return False
        return(True)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Draw a spine following your design.")

        split = layout.split(factor=0.8)
        col_left = split.column()
        col_right = split.column()


        col_left.alignment='LEFT'
        row_left = col_left.row()
        row_left.alignment='LEFT'
        row_left.operator("wm.draw_straight_lines", text="", icon="LINE_DATA")
        row_left.operator("wm.draw_freehand", text="", icon="GREASEPENCIL")
        row_left.label(text="Drawing mode : "+drawing_mode)
        
        col_right.alignment='LEFT'
        row_right = col_right.row()
        row_right.alignment='RIGHT'
        row_right.operator("wm.clear_spine", text="", icon="TRASH")

class Panel_Generate_Volume(bpy.types.Panel):
    bl_label = "Generate Volume (Step 3)"
    bl_idname = "SPINELOFT_PT_GENVOL"
    bl_parent_id = "SPINELOFT_PT_SPINELOFT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category="Tool"
    
    @classmethod
    def poll(cls, context):
        if step<=1:
            return False
        return(True)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Generate your volume.")

        row = layout.row()
        row.operator("wm.gen_vol", text="Generate 3D Volume")





def register():
    bpy.utils.register_class(Panel_SpineLoft)
    bpy.utils.register_class(Panel_Select_Image)
    bpy.utils.register_class(Panel_Draw_Tools)
    bpy.utils.register_class(Panel_Generate_Volume)
    bpy.utils.register_class(Operator_Select_Image)
    bpy.utils.register_class(Operator_Draw_FH)
    bpy.utils.register_class(Operator_Draw_SL)
    bpy.utils.register_class(Operator_Clear_Spine)
    bpy.utils.register_class(Operator_Generate_Volume)

def unregister():
    bpy.utils.unregister_class(Panel_SpineLoft)
    bpy.utils.unregister_class(Panel_Select_Image)
    bpy.utils.unregister_class(Panel_Draw_Tools)
    bpy.utils.unregister_class(Panel_Generate_Volume)
    bpy.utils.unregister_class(Operator_Select_Image)
    bpy.utils.unregister_class(Operator_Draw_FH)
    bpy.utils.unregister_class(Operator_Draw_SL)
    bpy.utils.unregister_class(Operator_Clear_Spine)
    bpy.utils.unregister_class(Operator_Generate_Volume)



def move_view3d_to(location=(0,0,0), rotation=(0, 0, 0)):

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':


                    region_3d = area.spaces.active.region_3d
                    region_3d.view_location = mathutils.Vector(location)
                    # Rotation en radians (Euler XYZ)
                    region_3d.view_rotation = mathutils.Euler(rotation, 'XYZ').to_quaternion()
                    return


def create_ref_image(image_path):
    img = bpy.data.images.load(image_path)

    # Créer un empty image dans la scène
    empty_img = bpy.data.objects.new("Reference_Image", None)
    empty_img.empty_display_type = 'IMAGE'
    empty_img.data = None  # pas nécessaire pour empties
    empty_img.empty_display_size = 1

    # Assigner l'image à l'empty
    empty_img.data = img

    # Ajouter à la scène active
    bpy.context.collection.objects.link(empty_img)

    # Positionner l'empty image si besoin
    empty_img.location = (0, 0, 0)




def get_mouse_3d_location(context, event):
    # Récupérer la région et les données de la vue 3D
    region = context.region
    rv3d = context.region_data

    # Convertir les coordonnées 2D du curseur en coordonnées 3D
    coord = (event.mouse_region_x, event.mouse_region_y)

    # Direction du rayon, depuis la vue
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
    ray_direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)

    plane_no = mathutils.Vector((0, 0, 1))

    denom = ray_direction.dot(plane_no)
    if abs(denom) < 1e-6:
        # Le rayon est parallèle au plan XY, pas d’intersection
        return None

    d = -ray_origin.dot(plane_no) / denom
    if d < 0:
        # Intersection derrière la caméra
        return None

    hit_pos = ray_origin + d * ray_direction
    return hit_pos

def create_curve():
    global curve_data
    global curve_obj 
    global spline
    global list_points
    list_points=[]

    try:
        bpy.data.objects.remove(curve_obj, do_unlink=True)
        curve_obj=None
    except:
        pass

    if curve_data == None:
        curve_data = bpy.data.curves.new(name="Spine", type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.bevel_depth = 0.005
        
    curve_data.splines.clear()
    spline = curve_data.splines.new(type='POLY')
    spline.use_cyclic_u = False
    spline.points[0].hide=True

    

    curve_obj = bpy.data.objects.new("CurveObj", curve_data)
    bpy.context.window.scene.collection.objects.link(curve_obj)

def delete_curve():
    global curve_data
    global curve_obj 
    global spline
    global list_points
    list_points=[]

    try:
        bpy.data.objects.remove(curve_obj, do_unlink=True)
        curve_obj=None
        curve_data.splines.clear()
        curve_data=None
    except:
        pass


    
    curve_obj = bpy.data.objects.new("CurveObj", curve_data)
    bpy.context.window.scene.collection.objects.link(curve_obj)

def add_stroke_point(pos):
    global spline
    global list_points

    if spline.points[0].hide==False:
        spline.points.add(1)
    else:
        spline.points[0].hide=False
    
    point = spline.points[-1]
    point.co = (pos[0], pos[1], 0.01,1)  # Position du point
    
    list_points.append([pos[0], pos[1]])

def redistribute_stroke(stroke : list) -> list:
    ans = []
    threshold = 1e-3
    i = 0
    while i < len(stroke) - 1:
        for j in range(i + 1, len(stroke)):
            currVec = (stroke[j][0] - stroke[i][0], stroke[j][1] - stroke[i][1])
            if d2.length(currVec) > threshold:
                ans.append(stroke[i])
                break
        i = j
