import bpy
import subprocess
import sys



# Paramètres 

bl_info = {
    "name": "Spine Generator",
    "blender": (2, 90, 0),  # La version de Blender compatible
    "category": "3D View",  # Catégorie sous laquelle l'addon apparaît (peut être View3D, Object, etc.)
    "author": "Télécom Paris",
    "version": (1, 0),
    "description": "Addon de test.",
    "warning": "",
    "doc_url": "",  # URL vers la documentation si nécessaire
    "tracker_url": "",  # URL vers un tracker de bugs si nécessaire
    "support": "COMMUNITY",  # Peut être "COMMUNITY" ou "OFFICIAL"
}






#Partie UI
class Operator_CreateSpine(bpy.types.Operator):
    bl_idname = "operator.createspine"  # L'ID unique de l'opérateur
    bl_label = "Create a spine"
    
    
    def execute(self, context):
        create_spine(points_list)  # Exécute l'opérateur pour ajouter un cube
        return {'FINISHED'}
    
    

class Panel_PhotoSketching(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Photo Sketching"
    bl_idname = "panel.photosketching"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Super Spine Generator 2000", icon='CURVE_PATH')
        
        row = layout.row()
        row.operator("operator.findfile")
        
        row = layout.row()
        row.operator("operator.showpicture")
        
        row = layout.row()
        row.operator("operator.createspine")
        
class Operator_ShowPicture(bpy.types.Operator):
    bl_idname = "operator.showpicture"
    bl_label = "Affichage d'une image"
    
    

    def execute(self, context):
        open_new_window()
        return {'FINISHED'}



# Initialisation

def register():
    bpy.utils.register_class(Panel_PhotoSketching)
    bpy.utils.register_class(Operator_CreateSpine)
    bpy.utils.register_class(Operator_ShowPicture)



def unregister():
    bpy.utils.unregister_class(Panel_PhotoSketching)
    bpy.utils.unregister_class(Operator_CreateSpine)
    bpy.utils.unregister_class(Operator_ShowPicture)



if __name__ == "__main__":
    register()






# Code


points_list = [((-1)**k,k) for k in range(10)]

def create_spine(points_list):
    l=len(points_list)
    
    crv = bpy.data.curves.new('spine', 'CURVE') #Créé un espace de donnée dans Blender pour la colonne vertébrale
    crv.dimensions = '3D'
    
    spine = crv.splines.new(type='POLY') #Créé la colonne vertébrale (vide)
    
    spine.points.add(l-1) #On ajoute les points de la courbe (il y en a 1 de base) et on les met au bon endroit
    for i in range(l):
        spine.points[i].co = (points_list[i]+(0,1)) #SplinePoint est un vecteur à 4 dimensions (3 coordonnées + poids du vecteur). Comme on travaille en 2D, on rajoute 0 en z et un poids de 1
    spine.use_cyclic_u = False
    spine.use_cyclic_v = False      
        
        
    #Ajoute l'objet dans la courbe actuelle 
    obj = bpy.data.objects.new('Spine', crv)
    collection = bpy.context.collection
    collection.objects.link(obj)


def open_new_window():
    
     # Création d'une nouvelle fenêtre en mode 'WINDOW'
    
    window = bpy.ops.wm.window_new()
    bpy.context.area.type='IMAGE_EDITOR'
    bpy.context.area.show_menus=False
    bpy.context.area.header_text_set("Draw your spine")