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

ribs=None

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

class Operator_Generate_Ribs(bpy.types.Operator):
    """Generate your ribs."""
    bl_idname = "wm.gen_ribs"
    bl_label = "Generate 3ribs"
    
    def invoke(self, context, event):
        global step
        global ribs
        ratio = max (image_width,image_height)

        image_dest=[0]*image_height*image_width
        for i in range(0,image_width*image_height*4,4):
            r = pixels[i]
            g = pixels[i+1]
            b = pixels[i+2]
            image_dest[i//4]=int((r*0.2989+g*0.587+b*0.114)*255)

        nb_ribs=bpy.context.scene.rib_number
        new_stroke = redistribute_stroke(list_points,nb_ribs)
        list_points_denormalized=[(p[0]*ratio+image_width/2, -(p[1]*ratio-image_height/2)) for p in new_stroke]

        accuracy=bpy.context.scene.accuracy_slider
        init_rib_size=bpy.context.scene.init_rib_size
        rib_step=bpy.context.scene.rib_step
        ribs = intersect.intersect(image_width, image_height, image_dest, list_points_denormalized, [], accuracy, init_rib_size,rib_step)
        

        
        edges_list = []
        for i in range(len(ribs)):
            # a verifier le [i][0][0] pour le format de retour de intersect
            x1 = ribs[i][0][0]
            y1 = ribs[i][0][1]

            x2 = ribs[i][1][0]
            y2 = ribs[i][1][1]

            xd1 = (x1 - image_width/2)/ratio 
            yd1 = (image_height/2-y1) /ratio
            xd2 = (x2 - image_width/2)/ratio 
            yd2 = (image_height/2-y2) /ratio

            edges_list.append((xd1, yd1, 0))
            edges_list.append((xd2, yd2, 0))

        

        #Création de la zone de data liée au volume
        crcl = bpy.data.meshes.new('circle')
        mesh=gen_vol.giveMeTheMesh(edges_list,0)

        crcl.from_pydata(mesh[0],mesh[1],mesh[2])
        ribs=crcl
        
        #Ajoute l'objet dans la collection actuelle 
        obj = bpy.data.objects.new('Circle', crcl)
        bpy.context.window.scene.collection.objects.link(obj)
        step=3
        return {'FINISHED'}

class Operator_Generate_Volume(bpy.types.Operator):
    """Generate your 3D volume."""
    bl_idname = "wm.gen_vol"
    bl_label = "Generate 3D Volume"
    
    def invoke(self, context, event):
        coords = [tuple(v.co.copy()) for v in ribs.vertices]
        print("coords=",coords)
        

        #Création de la zone de data liée au volume
        crcl = bpy.data.meshes.new('volume_spineloft')
        mesh=gen_vol.giveMeTheMesh(coords,1)
        crcl.from_pydata(mesh[0],mesh[1],mesh[2])
        
        #Ajoute l'objet dans la collection actuelle 
        obj = bpy.data.objects.new('SpineLoft', crcl)
        bpy.context.window.scene.collection.objects.link(obj)
        step=0
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

class Panel_Generate_Ribs(bpy.types.Panel):
    bl_label = "Generate Ribs (Step 3)"
    bl_idname = "SPINELOFT_PT_GENRIB"
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
        layout.label(text="Generate your ribs.")

        split = layout.split(factor=0.5)

        col_left = split.column()
        row1 = col_left.row()
        row1.prop(context.scene,'rib_number')
        row2 = col_left.row()
        row2.prop(context.scene,'accuracy_slider')
        

        col_right = split.column()
        row1 = col_right.row()
        row1.prop(context.scene,'init_rib_size')
        row2 = col_right.row()
        row2.prop(context.scene,'rib_step')

        row=layout.row()
        row.operator("wm.gen_ribs", text="Generate ribs")
    
class Panel_Generate_Volume(bpy.types.Panel):
    bl_label = "Generate Volume (Step 4)"
    bl_idname = "SPINELOFT_PT_GENVOL"
    bl_parent_id = "SPINELOFT_PT_SPINELOFT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category="Tool"
    
    @classmethod
    def poll(cls, context):
        if step<=2:
            return False
        return(True)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Generate your volume.")

        row=layout.row()
        row.operator("wm.gen_vol", text="Generate 3D Volume")




def register():
    bpy.utils.register_class(Panel_SpineLoft)
    bpy.utils.register_class(Panel_Select_Image)
    bpy.utils.register_class(Panel_Draw_Tools)
    bpy.utils.register_class(Panel_Generate_Ribs)
    bpy.utils.register_class(Panel_Generate_Volume)
    bpy.utils.register_class(Operator_Select_Image)
    bpy.utils.register_class(Operator_Draw_FH)
    bpy.utils.register_class(Operator_Draw_SL)
    bpy.utils.register_class(Operator_Clear_Spine)
    bpy.utils.register_class(Operator_Generate_Ribs)
    bpy.utils.register_class(Operator_Generate_Volume)
    register_prop()

def unregister():
    bpy.utils.unregister_class(Panel_SpineLoft)
    bpy.utils.unregister_class(Panel_Select_Image)
    bpy.utils.unregister_class(Panel_Draw_Tools)
    bpy.utils.unregister_class(Panel_Generate_Ribs)
    bpy.utils.unregister_class(Panel_Generate_Volume)
    bpy.utils.unregister_class(Operator_Select_Image)
    bpy.utils.unregister_class(Operator_Draw_FH)
    bpy.utils.unregister_class(Operator_Draw_SL)
    bpy.utils.unregister_class(Operator_Clear_Spine)
    bpy.utils.unregister_class(Operator_Generate_Ribs)
    bpy.utils.unregister_class(Operator_Generate_Volume)
    unregister_prop()



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

def redistribute_stroke(stroke : list, nb : int) -> list:
    # Calcul longueur totale
    L=d2.getSqrtA(stroke)**2


    # Nouvelle stroke
    l=L/nb
    pt_start=stroke[0]
    pt_next=stroke[1]


    i=0
    newStroke=[stroke[0]]
    
    for k in range(nb-2):
        l2=l
        d=d2.length((pt_next[0] - pt_start[0], pt_next[1] - pt_start[1]))
        while(l2>d):
            i+=1
            pt_next=stroke[i+1]
            pt_start=stroke[i]
            l2-=d
            d=d2.length((pt_next[0] - pt_start[0], pt_next[1] - pt_start[1]))

        
        pt_start=[pt_start[0] + l2* (pt_next[0] - pt_start[0])/d, pt_start[1] + l2* (pt_next[1] - pt_start[1])/d]
        newStroke.append( pt_start )
        

    newStroke.append(stroke[-1])
    return(newStroke)

    # ans = []
    # threshold = 1e-3
    # i = 0
    # while i < len(stroke) - 1:
    #     for j in range(i + 1, len(stroke)):
    #         currVec = (stroke[j][0] - stroke[i][0], stroke[j][1] - stroke[i][1])
    #         if d2.length(currVec) > threshold:
    #             ans.append(stroke[i])
    #             break
    #     i = j
    # return(ans)


def register_prop():
    bpy.types.Scene.accuracy_slider = bpy.props.FloatProperty(
        name="Contouring accuracy",
        description="Choose an accuracy for your contouring.",
        default=50,
        min=1.0,
        max=250
    )

    bpy.types.Scene.init_rib_size = bpy.props.FloatProperty(
        name="Initial rib size",
        description="Choose a size that define the initial length of your ribs.",
        default=2,
        min=0.5,
        max=10
    )

    bpy.types.Scene.rib_step = bpy.props.FloatProperty(
        name="Rib steps size",
        description="Choose the size of the steps in the rib-creation process. \n(small=accurate, large=fast)",
        default=1,
        min=0.4,
        max=5
    )

    bpy.types.Scene.rib_number = bpy.props.IntProperty(
        name="Maximum number of ribs",
        description="Choose the maximum number of ribs",
        default=20,
        min=5,
        max=500
    )

    bpy.types.Scene.choose_shape = bpy.props.EnumProperty(
    name="Shape",
    description="Choose a shape to extrude",
    items=[
        ("Circle", "Circle", ""),
        ("Square", "Square", ""),
    ],
    default='Circle'
    )


def unregister_prop():
    del bpy.types.Scene.accuracy_slider