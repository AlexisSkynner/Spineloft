####################################
import subprocess
import sys
import bpy


path=bpy.utils.user_resource("SCRIPTS", path="modules")
sys.path.append(path)

def printError(self, context):
    self.layout.label(text="Required modules cannot be installed. Try again while running Blender as administrator. Desired path = "+path)


#numpy
try:
    import matplotlib.pyplot as plt
    print("numpy is already installed")

except:
    print("numpy is not available in "+path+". Installation...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--target", path, "matplotlib", "--upgrade"])
    except:
        print("numpy cannot be installed in "+path+". Try running Blender as administrator.")
        bpy.context.window_manager.popup_menu(printError, title="Error", icon='ERROR')





import numpy as np

####################################