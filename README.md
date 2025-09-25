Spineloft is a Blender add-on set to help their users creating a 3D model from a 2D sketch/image in the process of sculpting or 3D design. 

The differents steps are the following : 

### STEP 1 : opening the add-on and importing the image. 

In Edit/Preferences/Add ons click on the arrow facing down and Install from Disk the .zip file. 
Then you will find the add-on the Tool pannel as Spineloft tool.
From there you can open an image.

### STEP 2 : Drawing the spine.

This step is the most important one. From the part of the image you want to transform in 3D, draw with freehand or straight lines drawing a line called the spine. From this line will be computed "ribs" creating the skeleton of the form. 
Moreover, you have the option to create a non-contour area. From this tool, you can draw a contour in which no contour can be detected. This is a way to avoid details that are not the contour of your image which may create uncoherente ribs. 

### Step 3 : Generate the ribs.

In order to generate the ribs that will form the skeleton of your 3D model, you need to adjust some parameters. 
- Maximum number of ribs : this allow you to choose the number of ribs that will be created. 
- Contouring accuracy : this parameter set the strenght of the contouring algorithm that detects the contour of the image. The stronger it is, the less imperfection you will have but this may lead to the disparation of some part of the wnating contour. This parameter can be set from 5 to 20 for simple distinct model, up to more than 100 for real image with details 
- Initial rib size : this parameter set the minimal distance of the rib. Going too low may end up creating some wrong ribs. Over 0.5 is generally fine. 
- Rib steps size : This parameter impact de ribs computing process. It sets the length of the steps of searching the contour from the spine. The higher it is, the less the computing time will be but this may lead to crossing a contour without noticing it. Therefore, the lower its value is, the longer it will take but your reducing the chance of skipping a contour. Setting it to 1.0 is usually fine.

### Step 4 : Generate the volume.

Once the ribs are created, you can adjust them by dragging them to the place you want them to be. When your satisfied of the skeleton you can create the volume by choosing a preset shape or by creating your own with custom shape. Then generate it. 

As a tutorial, you can click on the following link : 

https://youtube.com/..

The code is a research prototype, is not complete, and may contain errors. Please see the demo video to see how to use the plugin. Use it responsibly, as the authors and developers cannot be held liable for any issues.
