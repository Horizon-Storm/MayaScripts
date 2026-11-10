import maya.cmds as cmds

# This script is to try to select all the parent constraints to swap their interpolation types

# Find all parentConstraint nodes in the current Maya scene.
constraints = cmds.ls(type='parentConstraint')

# Replace the current selection with the found constraints.
cmds.select(constraints, r=True)
