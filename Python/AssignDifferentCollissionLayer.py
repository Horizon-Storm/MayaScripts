#This script again iterates over a selection and sets each object to have a different Collision Layer
#Its useful for speeding up things like brick wall explosions where the inter-object collisions aren't really important.
#Remember to set you impact object and ground plane to Collision Layer -1 so that it still collides with everything. 

import maya.cmds as cmds

# save selection as a list 
sel = cmds.ls(sl=True)

# iterate over items in the list setting each to have a different Collision Layer
for i in range(len(sel)):
    cmds.setAttr('{0}.collisionLayer'.format(sel[i]), i)