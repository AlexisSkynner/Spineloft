import bpy
import functools
import bpy_extras
from bpy_extras import view3d_utils
from . import gen_vol
import mathutils
import blf
import gpu
from gpu_extras.batch import batch_for_shader
from pathlib import Path
import numpy as np
from . import intersect



name="tp.fr.spineloft.customviewerscene"
curve_data=0
curve_obj = 0
spline = 0
list_points=[]
override=0
is_open=False
overlay_state={}
is_drawing=False
image=None
handle=None
tex_image=0
drawing_mode="None"
part=0
old_scene=None
image_width=0
image_height=0

###########################################################################################################################################
def createWindow():

     # Création de la nouvelle scene et de la caméra #############################################
    for scene in bpy.data.scenes:
         if scene.name==(name):
              bpy.data.scenes.remove(scene)

    # Scène
    blank_scene = bpy.data.scenes.new("tp.fr.spineloft.customviewerscene")
    blank_scene.render.resolution_x = 1024
    blank_scene.render.resolution_y = 1024

    #Caméra
    cam_data = bpy.data.cameras.new(name)
    cam_data.show_passepartout = False
    cam_data.type = 'ORTHO'  # Pas de perspective
    cam_data.ortho_scale = 1.0
    cam_obj = bpy.data.objects.new("Camera", cam_data)
    blank_scene.collection.objects.link(cam_obj)


    cam_obj.location = (0, 0, 1)
    cam_obj.rotation_euler = (0, 0, 0)

    blank_scene.camera = cam_obj
    ###########################################################################


    ############## Affichage de la scène concernée ###########
    global old_scene
    old_scene=bpy.context.scene
    
    area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
    region = next(region for region in area.regions if region.type == 'WINDOW')
    space = next(space for space in area.spaces if space.type == 'VIEW_3D')

    global override
    override = {
        'window': bpy.context.window,
        'screen': bpy.context.screen,
        'area': area,
        'region': region,
        'scene': bpy.data.scenes[name],
        'space_data': space,
    }


    bpy.context.window.scene = bpy.data.scenes[name]
    save_overlay_state(space)
    space.lock_camera = True  # Verrouiller la caméra dans la vue
    space.overlay.show_axis_x = False  
    space.overlay.show_axis_y = False  
    space.overlay.show_axis_z = False  
    space.overlay.show_overlays = False
    space.show_gizmo = False
    space.show_region_header = False
    space.show_region_toolbar = False
    space.show_region_ui = False
    space.shading.type = 'MATERIAL'
    
    ###############################################################""

    

    #### Image de reference ##################################################################""
    
    with bpy.context.temp_override(window=override["window"],area=override["area"],region=override["region"]):
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    global plane
    plane = bpy.context.active_object
    plane.name = "ImagePlane"

    # Créer un nouveau matériel
    mat = bpy.data.materials.new(name="ImageMaterial")
    mat.use_nodes = True

    bsdf = mat.node_tree.nodes["Principled BSDF"]

    # Ajouter un node image texture
    global tex_image
    tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')

    # Connecter le node image au BSDF
    mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

    # Assigner le matériel au plane
    plane.data.materials.append(mat)
    ###############################################################################################################


    #### Spine ####################################################################################################
    # Créer un objet curve
    global curve_data
    curve_data = bpy.data.curves.new(name="Spine", type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = 0.005

    create_spline(curve_data)
    ###############################################################################################################

    ### Start the UI ###################################################################################################################
    global is_open
    global handle
    global part
    part=0
    is_open=True
    bpy.app.timers.register(functools.partial(scene_manager,old_scene))
    handle = bpy.types.SpaceView3D.draw_handler_add(draw_buttons, (None,override), 'WINDOW', 'POST_PIXEL')
    with bpy.context.temp_override(window=override["window"],area=override["area"],region=override["region"]):
        bpy.ops.view3d.ui_manager('INVOKE_DEFAULT')
    return
###########################################################################################################################################


### Lock camera view ############################################################################
def set_camera_view():
    area = override["area"]
    space = area.spaces.active
    space.region_3d.view_perspective = 'CAMERA'  # Vue caméra
    space.lock_camera = True  # Verrouiller la caméra dans la vue   
    bpy.context.scene.camera.location = (0, 0, 1)
    bpy.context.scene.camera.rotation_euler = (0, 0, 0)

#################################################################################################





########### Gestion de la fermeture de la fenêtre ###############################################
def scene_manager(old_scene):
    if override==0:
        return(0.1)
    
    global is_open
    global handle

    if is_open:
        set_camera_view()
        override["area"].tag_redraw()
        return 0.01
    


    else:  

        bpy.context.window.scene = old_scene
        for scene in bpy.data.scenes:
            if scene.name==(name):
                bpy.data.scenes.remove(scene)

        bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')
        handle = None
        override["area"].tag_redraw()

        space=override["area"].spaces[-1]
        restore_overlay_state(space)

#################################################################################################






###### Détecteur de click et tracage de spine ###################################################

def get_mouse_3d_location(context, event):
    # Récupérer la région et les données de la vue 3D
    region = context.region
    rv3d = context.region_data

    # Convertir les coordonnées 2D du curseur en coordonnées 3D
    coord = (event.mouse_region_x, event.mouse_region_y)

    # Direction du rayon, depuis la vue
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
    ray_origin =  mathutils.Vector((ray_origin[0],ray_origin[1],1))


    return ray_origin, view_vector

#################################################################################################







# Coordonnées du "bouton" (x, y, largeur, hauteur)
def button_rect():
    rect=[0, 0, 0.05, 0.05]
    if override:
        width=override["region"].width
        height=override["region"].height
        rect[2]*=width
        rect[3]*=width
        rect[0]=width-rect[2]
        rect[1]=height-rect[3]

    return(rect)


gray_color = (40/255,40/255,40/255,1)
red_color = (237/255,55/255,81/255,1)
dark_red_color=(215/255,45/255,72/255,1)
blue_color = (71/255,114/255,179/255,1)
light_gray_color=(48/255,48/255,48/255,1)
green_color=(140/255, 210/255, 25/255,1)
light_green_color=(160/255,230/255,45/255,1)
blue_color=(56/255,76/255,132/255,1)
buttons_color_original=[red_color,gray_color,gray_color,gray_color,gray_color,green_color]
buttons_color_over=[dark_red_color,light_gray_color,light_gray_color,light_gray_color,light_gray_color,light_green_color]
buttons_color_selected=[dark_red_color,blue_color,blue_color,blue_color,blue_color,light_green_color]
buttons_color=[red_color,gray_color, gray_color,gray_color,gray_color,green_color]

# Dessin du bouton (rectangle simple)
def draw_buttons(a,b):
    global part

    # Fonts
    path_to_font_emoji=str(Path(__file__).parent / "font" / "NotoEmoji-Bold.ttf")
    font_emoji = blf.load(path_to_font_emoji)

    if part==0:
        #Button 0
        x, y, w, h = button_rect()
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        coords = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coords})
        gpu.state.blend_set('ALPHA')
        shader.bind()
        shader.uniform_float("color", buttons_color[0])  
        batch.draw(shader)
        gpu.state.blend_set('NONE')

        blf.position(font_emoji, x+w/5, y+w/3, 0)
        blf.size(font_emoji, w/2)
        blf.color(font_emoji, 1.0, 1.0, 1.0, 1.0)
        blf.draw(font_emoji, "✖︎")

        #Button 1
        y-=w
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        coords = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coords})
        gpu.state.blend_set('ALPHA')
        shader.bind()
        shader.uniform_float("color", buttons_color[1])  
        batch.draw(shader)
        gpu.state.blend_set('NONE')

        
        blf.position(font_emoji, x+w/5, y+w/3, 0)
        blf.size(font_emoji, w/2)
        blf.color(font_emoji, 1.0, 1.0, 1.0, 1.0)
        blf.draw(font_emoji, "📁")

        #Button 2
        y-=w
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        coords = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coords})
        gpu.state.blend_set('ALPHA')
        shader.bind()
        shader.uniform_float("color", buttons_color[2])  
        batch.draw(shader)
        gpu.state.blend_set('NONE')

        blf.position(font_emoji, x+w/5, y+w/3, 0)
        blf.size(font_emoji, w/2)
        blf.color(font_emoji, 1.0, 1.0, 1.0, 1.0)
        blf.draw(font_emoji, "📏")

        #Button 3
        y-=w
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        coords = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coords})
        gpu.state.blend_set('ALPHA')
        shader.bind()
        shader.uniform_float("color", buttons_color[3])  
        batch.draw(shader)
        gpu.state.blend_set('NONE')

        blf.position(font_emoji, x+w/5, y+w/3, 0)
        blf.size(font_emoji, w/2)
        blf.color(font_emoji, 1.0, 1.0, 1.0, 1.0)
        blf.draw(font_emoji, "✒︎")

        #Button 4
        y-=w
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        coords = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coords})
        gpu.state.blend_set('ALPHA')
        shader.bind()
        shader.uniform_float("color", buttons_color[4])  
        batch.draw(shader)
        gpu.state.blend_set('NONE')

        blf.position(font_emoji, x+w/5, y+w/3, 0)
        blf.size(font_emoji, w/2)
        blf.color(font_emoji, 1.0, 1.0, 1.0, 1.0)
        blf.draw(font_emoji, "🧹")

        #Button 5
        y-=w
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        coords = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coords})
        gpu.state.blend_set('ALPHA')
        shader.bind()
        shader.uniform_float("color", buttons_color[5])  
        batch.draw(shader)
        gpu.state.blend_set('NONE')

        blf.position(font_emoji, x+w/5, y+w/3, 0)
        blf.size(font_emoji, w/2)
        blf.color(font_emoji, 1.0, 1.0, 1.0, 1.0)
        blf.draw(font_emoji, "✔︎")

        # Drawing mode
        blf.position(0, w/5, w/5, 0)
        blf.size(0, w/5)
        blf.color(0, 1.0, 1.0, 1.0, 1.0)
        blf.draw(0, "Drawing mode = " + drawing_mode)

    elif part==1:
        #Button 0
        x, y, w, h = button_rect()
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        coords = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coords})
        gpu.state.blend_set('ALPHA')
        shader.bind()
        shader.uniform_float("color", buttons_color[0])  
        batch.draw(shader)
        gpu.state.blend_set('NONE')

        blf.position(font_emoji, x+w/5, y+w/3, 0)
        blf.size(font_emoji, w/2)
        blf.color(font_emoji, 1.0, 1.0, 1.0, 1.0)
        blf.draw(font_emoji, "✖︎")

        #Button 1
        y-=w
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        coords = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coords})
        gpu.state.blend_set('ALPHA')
        shader.bind()
        shader.uniform_float("color", buttons_color[5])  
        batch.draw(shader)
        gpu.state.blend_set('NONE')

        blf.position(font_emoji, x+w/5, y+w/3, 0)
        blf.size(font_emoji, w/2)
        blf.color(font_emoji, 1.0, 1.0, 1.0, 1.0)
        blf.draw(font_emoji, "✔︎")

# Affichage de l'UI et gestion des inputs
class Operator_UImanager(bpy.types.Operator):
    bl_idname = "view3d.ui_manager"
    bl_label = "HUD Bouton"

    def modal(self, context, event):
        global is_open
        global drawing_mode

        if part==0:
            self.part1_button_manager(context,event)
            self.part1_tool_manager(context,event)
        
        elif part ==1:
            self.part2_button_manager(context,event)
        
        if not is_open:
            return{'FINISHED'}

        if drawing_mode=="None":
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}


    def part1_button_manager(self,context,event):
        global is_drawing
        global is_open
        global buttons_color
        global list_points
        global drawing_mode
        global part
        # Buttons
        if self.click_on_button(context,event,0):
            is_open=False
            is_drawing=False
            drawing_mode="None"

            
        if self.click_on_button(context,event,1):
            with bpy.context.temp_override(window=override["window"],area=override["area"],region=override["region"]):
                bpy.ops.wm.open_file_selector('INVOKE_DEFAULT')


        if self.click_on_button(context,event,2):
            if drawing_mode!="Line":
                drawing_mode="Line"
            else:
                drawing_mode="None"
        
        if self.click_on_button(context,event,3):
            if drawing_mode!="Free hand":
                drawing_mode="Free hand"
            else:
                drawing_mode="None"

        if self.click_on_button(context,event,4):
            is_drawing=False
            drawing_mode="None"
            create_spline(curve_data)

        if self.click_on_button(context,event,5):     
            print (list_points)
            is_drawing=False
            drawing_mode="None"
            
            # Récupérer les contours ########################################
            # edges_list=[ [(1,1,0),(2,1,0)] , [(1,3,0),(2,2,0)], [(4,4,0), (4,3,0)]] #Liste des points de la forme, 
            # list_points = [[1,1],[2,1],[3,4]]
            # triés dans le sens horraire
            ################################################################
            ratio_x = min(1, image_width / image_height)
            ratio_y = min(1, image_height / image_width)

            img = []
            for i in range(0, image_width * image_height, 4):
                print(i)
                r = image.pixels[i]
                g = image.pixels[i + 1]
                b = image.pixels[i + 2]
                img.append(int(255 * (r * r + g * g + b * b) / 195075))
            ribs = intersect.intersect(image_width, image_height, img, [(p[0] / ratio_x + 0.5, 0.5 - p[1] / ratio_y) for p in list_points])

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

                edges_list.append((xd1, yd1, 0))
                edges_list.append((xd2, yd2, 0))

            #Création de la zone de data liée au volume
            crcl = bpy.data.meshes.new('circle')
            mesh=gen_vol.giveMeTheMesh(edges_list)
            crcl.from_pydata(mesh[0],mesh[1],mesh[2])
            
            #Ajoute l'objet dans la collection actuelle 
            obj = bpy.data.objects.new('Circle', crcl)
            old_scene.collection.objects.link(obj)
            is_open=False
                #part=1
        
        if event.type == 'ESC':
            is_drawing=False
            drawing_mode="None"
                
        # Is over
        for i in range(6):
            
            if self.is_over_button(context,event,i):
                buttons_color[i]=buttons_color_over[i]
            else:
                buttons_color[i]=buttons_color_original[i]

            if drawing_mode=="Line":
                buttons_color[2]=buttons_color_selected[2]

            elif drawing_mode=="Free hand":
                buttons_color[3]=buttons_color_selected[3]



        override["area"].tag_redraw()

    def part2_button_manager(self,context,event):
        global is_open
        if self.click_on_button(context,event,0):
            is_open=False

        if self.click_on_button(context,event,1):
            is_open=False




    def part1_tool_manager(self,context,event):
        global is_drawing
        global list_points
        global drawing_mode
        global spline
        #Line
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and drawing_mode=="Line":
            # Récupérer la position du rayon (origine + direction)
            ray_origin, view_vector = get_mouse_3d_location(context, event)

            # Calculer où le rayon touche dans la scène
            depsgraph = bpy.context.evaluated_depsgraph_get()
            result, location, normal, index, obj, matrix = context.scene.ray_cast(
                depsgraph,
                ray_origin,
                view_vector
            )

            # Si on touche un objet, on peut ajouter un cube ou autre à l'endroit du clic
            if result:

                if spline.points[0].hide!=True:
                    spline.points.add(1)  # Un seul point (0 car 1 par défaut)

                else:
                    spline.points[0].hide=False

                point = spline.points[-1]
                point.co = (location[0], location[1], 0.1,1)  # Position du point
                
                list_points.append([location[0], location[1]])
            



        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and drawing_mode=="Free hand" and is_drawing==False:
            is_drawing=True

        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE' and drawing_mode=="Free hand" and is_drawing:
            is_drawing=False

        
        if is_drawing:
            # Récupérer la position du rayon (origine + direction)
            ray_origin, view_vector = get_mouse_3d_location(context, event)

            # Calculer où le rayon touche dans la scène
            depsgraph = bpy.context.evaluated_depsgraph_get()
            result, location, normal, index, obj, matrix = context.scene.ray_cast(
                depsgraph,
                ray_origin,
                view_vector
            )

            if result:

                if spline.points[0].hide!=True:
                    spline.points.add(1)  # Un seul point (0 car 1 par défaut)

                else:
                    spline.points[0].hide=False

                point = spline.points[-1]
                point.co = (location[0], location[1], 0.1,1)  # Position du point
                
                list_points.append([location[0], location[1]])
   



    def invoke(self, context, event=None):
        context.window_manager.modal_handler_add(self)

        global drawing_mode
        global is_drawing
        is_drawing=False
        drawing_mode="None"

        return {'RUNNING_MODAL'}

    def click_on_button(self,context,event, n):
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            x, y, w, h = button_rect()
            mx, my = event.mouse_region_x, event.mouse_region_y
            if x <= mx <= x + w and y-n*h <= my <= y + h - n*h:
                return True
        return(False)
    
    def is_over_button(self,context,event, n):
        x, y, w, h = button_rect()
        mx, my = event.mouse_region_x, event.mouse_region_y
        if x <= mx <= x + w and y-n*h <= my <= y + h - n*h:
                return True
        return(False)









def save_overlay_state(space):
    global overlay_state 
    overlay_state= {
        'show_axis_x': space.overlay.show_axis_x,
        'show_axis_y': space.overlay.show_axis_y,
        'show_axis_z': space.overlay.show_axis_z,
        'show_overlays': space.overlay.show_overlays,
        'show_gizmo': space.show_gizmo,
        'show_region_header': space.show_region_header,
        'show_region_toolbar': space.show_region_toolbar,
        'show_region_ui': space.show_region_ui,
        'lock_camera' :  space.lock_camera
    }

def restore_overlay_state(space):
    global overlay_state 
    space.overlay.show_axis_x = overlay_state['show_axis_x']
    space.overlay.show_axis_y = overlay_state['show_axis_y']
    space.overlay.show_axis_z = overlay_state['show_axis_z']
    space.overlay.show_overlays = overlay_state['show_overlays']
    space.show_gizmo = overlay_state['show_gizmo']
    space.show_region_header = overlay_state['show_region_header']
    space.show_region_toolbar = overlay_state['show_region_toolbar']
    space.show_region_ui = overlay_state['show_region_ui']
    space.lock_camera = overlay_state['lock_camera']



class Operator_SetBackgroundImage(bpy.types.Operator):
    bl_idname = "wm.open_file_selector"
    bl_label = "Sélectionner un fichier"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    global tex_image
    global plane
    

    def execute(self, context):
        global image
        global image_width
        global image_height
        image = bpy.data.images.load(self.filepath)
        tex_image.image=image

        size=image.size
        i=np.argmax(size)
        width=size[0]/size[i]
        height=size[1]/size[i]
        plane.scale = (width,height,1)

        image_width=size[0]
        image_height=size[1]
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)  # ouvre la fenêtre de fichier
        return {'RUNNING_MODAL'}



def create_spline(curve_data):
    # Ajouter une spline avec 1 point
    global spline
    global curve_obj
    global list_points
    list_points=[]
    
    if curve_obj:
        bpy.data.objects.remove(curve_obj, do_unlink=True)
        curve_obj=0

    if spline:
        curve_data.splines.clear()
    spline = curve_data.splines.new(type='POLY')
    spline.points[0].hide=True
    spline.use_cyclic_u = False

    
    
    curve_obj = bpy.data.objects.new("CurveObj", curve_data)
    bpy.context.window.scene.collection.objects.link(curve_obj)
