import bpy
import importlib
import addon_utils

bl_info = {
    "name": "SpineLoft",
    "blender": (2, 90, 0),  # The compatible Blender version 
    "category": "3D View",  # Categorie in which the addon appears
    "author": "Télécom Paris",
    "version": (1, 1),
    "description": "Addon de test.",
    "warning": "",
    "doc_url": "",  # URL to the documentation if needed
    "tracker_url": "",  # URL to a bug tracker if needed 
    "support": "COMMUNITY",  # Can be "COMMUNITY" or "OFFICIAL"
}

def register():

    everythingIsOkay=True

    try: #we try to install all libraries
        
        
        from . import register_script
        if "register_script" in locals():
            importlib.reload(register_script)


        from . import gen_vol 
        if "gen_vol" in locals():
            importlib.reload(gen_vol)

        
        from . import tool 
        if "tool" in locals():
            importlib.reload(tool)

        from . import intersect 
        if "intersect" in locals():
            importlib.reload(intersect)
        
        from . import d2 
        if "d2" in locals():
            importlib.reload(d2)

        

    except: 
        everythingIsOkay=False
        raise KeyboardInterrupt()


    if everythingIsOkay:
        register_script.register_all()

    else:
        addon_utils.disable('blender_addon', default_set=True)
    




def unregister():
    try:
       from . import register_script
       register_script.unregister_all()
    except:
       pass
       



