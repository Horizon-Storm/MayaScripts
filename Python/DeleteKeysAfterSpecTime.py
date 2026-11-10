#This script iterates over a selection and only keeps a set number of keyframes after the object first moves vertically. 
#This is useful for creating 'ground crack' style simulations - 
# simulate your pieces being impacted without gravity and then just keep the first 10-20 frames of the simulation

import maya.cmds as cmds
import math

# setup inital variables 
# Frame range to inspect, number of frames to retain after movement, and movement threshold.
start_frame = 0.0
last_frame = 200
frames_to_keep = 20.0
move_tolerance = 0.1

# list selected objects
# Read the current Maya selection for processing.
sel = cmds.ls(sl=1)

# iterate over each mesh in list
# Analyze and trim the animation of each selected object.
for mesh in sel:
    
    # re-initalalise
    # Reset the detected start frame and return the timeline to frame zero.
    print mesh 
    start_frame = 0.0
    cmds.currentTime(start_frame)
    
    # find the first frame the mesh moves 
    # Scan the timeline and record the time when vertical translation exceeds the threshold.
    for frame in range(last_frame):
        if not start_frame > 0:
            if cmds.getAttr('{0}.ty'.format(mesh)) > move_tolerance:
                start_frame = cmds.currentTime(query=1)
            cmds.currentTime(frame)
            
    # delete all frames after start_frame + frames_to_keep        
    # Remove keys after the chosen cutoff, up to the end of the scan range.
    cmds.cutKey('{0}'.format(mesh), time=(math.trunc(start_frame + frames_to_keep), last_frame))

# Leave the Maya timeline at the end of the inspected range.
cmds.currentTime(last_frame)