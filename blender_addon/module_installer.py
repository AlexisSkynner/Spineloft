####################################
import subprocess
import sys
import bpy
import importlib


path=bpy.utils.user_resource("SCRIPTS", path="modules")
sys.path.append(path)

def printError(self, context):
    self.layout.label(text="Required modules cannot be installed. Try again while running Blender as administrator. Desired path = "+path)


#pip
try:
    import pip
    print("pip is already installed")

except:
    print("pip is not available in "+path+". Installation...")
    try:
        import ensurepip
        ensurepip.bootstrap()
    except:
        print("pip" \ cannot be installed in "+path+". Try running Blender as administrator.")
        bpy.context.window_manager.popup_menu(printError, title="Error", icon='ERROR')

#pillow
try:
    import PIL
    print("Pillow is already installed")

except:
    print("Pillow is not available in "+path+". Installation...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        importlib.invalidate_caches()
        import PIL
    except:
        print("pip" \ cannot be installed in "+path+". Try running Blender as administrator.")
        bpy.context.window_manager.popup_menu(printError, title="Error", icon='ERROR')


####################################