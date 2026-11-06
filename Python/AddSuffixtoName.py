#Adds the specified suffix to the object names - useful for baking by name in Substance.


import maya.cmds as cmds

# Suffix text to add
suffix = '_low'

# List all selected objects
sel = cmds.ls(sl=1)

# For each item in the list add the suffix
for item in sel:
    cmds.rename(item,'{0}{1}'.format(item,suffix))