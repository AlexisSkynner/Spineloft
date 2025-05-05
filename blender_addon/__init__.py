import bpy
import importlib
import addon_utils

bl_info = {
    "name": "SpineLoft",
    "blender": (2, 90, 0),  # La version de Blender compatible
    "category": "3D View",  # Catégorie sous laquelle l'addon apparaît (peut être View3D, Object, etc.)
    "author": "Télécom Paris",
    "version": (1, 1),
    "description": "Addon de test.",
    "warning": "",
    "doc_url": "",  # URL vers la documentation si nécessaire
    "tracker_url": "",  # URL vers un tracker de bugs si nécessaire
    "support": "COMMUNITY",  # Peut être "COMMUNITY" ou "OFFICIAL"
}



    


def register():

    everythingIsOkay=True

    try: #On essaie d'installer les différentes librairies
        
        from . import module_installer
        if "module_installer" in locals():
            importlib.reload(module_installer)
        
        from . import register_script
        if "register_script" in locals():
            importlib.reload(register_script)

        from . import ui
        if "ui" in locals():
            importlib.reload(ui)

        from . import gen_vol 
        if "gen_vol" in locals():
            importlib.reload(gen_vol)

        from . import custom_editor 
        if "custom_editor" in locals():
            importlib.reload(custom_editor)

        

    except: #Si ça marche pas, on désactive le module.
        everythingIsOkay=False
        raise KeyboardInterrupt()


    if everythingIsOkay:
        register_script.register_all()

    else:
        addon_utils.disable('blender_addon', default_set=True)
        print(addon_utils.check('blender_addon'))
    




def unregister():
    try:
       from . import register_script
       register_script.unregister_all()
    except:
       pass
       



