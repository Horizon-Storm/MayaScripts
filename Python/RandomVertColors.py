
#Random Vertex Colours (default is Red channel only) 

import maya.cmds as cmds
import random

# Get the objects currently selected in Maya.
sel = cmds.ls(sl=1)

# Assign a random red-channel value to each selected object.
for item in sel:
    # Generate a random value between 0 and 1 for the red color channel.
    colour = random.random()
    # Select this item so Maya applies the color to the correct object.
    cmds.select(item)     
    # Set the object's per-vertex red color to the generated value.
    cmds.polyColorPerVertex(r=colour)