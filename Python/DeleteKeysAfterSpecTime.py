#This script iterates over a selection and only keeps a set number of keyframes after the object first moves vertically. 
#This is useful for creating 'ground crack' style simulations - 
# simulate your pieces being impacted without gravity and then just keep the first 10-20 frames of the simulation

import maya.cmds as cmds
import math

# setup inital variables 
start_frame = 0.0
last_frame = 200
frames_to_keep = 20.0
move_tolerance = 0.1

# list selected objects
sel = cmds.ls(sl=1)

# iterate over each mesh in list
for mesh in sel:
    
    # re-initalalise
    print mesh 
    start_frame = 0.0
    cmds.currentTime(start_frame)
    
    # find the first frame the mesh moves 
    for frame in range(last_frame):
        if not start_frame > 0:
            if cmds.getAttr('{0}.ty'.format(mesh)) > move_tolerance:
                start_frame = cmds.currentTime(query=1)
            cmds.currentTime(frame)
            
    # delete all frames after start_frame + frames_to_keep        
    cmds.cutKey('{0}'.format(mesh), time=(math.trunc(start_frame + frames_to_keep), last_frame))

cmds.currentTime(last_frame)