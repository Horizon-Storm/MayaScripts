import maya.cmds as cmds

# This script is to try to select all the parent constraints to swap their interpolation types

constraints = cmds.ls(type='parentConstraint')
cmds.select(constraints, r=True)
