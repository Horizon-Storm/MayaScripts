
#Random Vertex Colours (default is Red channel only) 

import maya.cmds as cmds
import random

sel = cmds.ls(sl=1)

for item in sel:
    colour = random.random()
    cmds.select(item)     
    cmds.polyColorPerVertex(r=colour)