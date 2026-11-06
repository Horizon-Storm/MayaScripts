#Sort objects in the Outliner Alphabetically

import maya.cmds as cmds

#Select all Geometry and reverse
sel = cmds.ls(tr=1) 
sel.reverse
#print sel

#Create an Empty Group
cmds.group(em=1, name='temp')

#Parent to the Empty Group and then back to World
for item in sel:
    cmds.parent('{0}'.format(item), 'temp')
    cmds.parent('{0}'.format(item), world=1)
    
#Select all Cameras 
sel = cmds.ls(ca=1) 

#Parent to the Empty Group and then back to World
for item in sel:
    cmds.parent('{0}'.format(item), 'temp')
    cmds.parent('{0}'.format(item), world=1)

#Delete the Empty Group    
cmds.delete('temp')