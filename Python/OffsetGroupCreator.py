#Creates offset group for rigging in maya.

import maya.cmds as cmds

def create_zero_group():
    """Creates a zero/offset group above the selected objects to freeze transform channels."""
    selection = cmds.ls(selection=True)
    if not selection:
        cmds.warning("Please select at least one object.")
        return
        
    for obj in selection:
        # Create a new group
        obj_parent = cmds.listRelatives(obj, parent=True)
        zero_grp = cmds.group(em=True, name=f"{obj}_zero")
        
        # Match group transform to object transform
        cmds.delete(cmds.parentConstraint(obj, zero_grp, maintainOffset=False))
        
        # If object had a parent, parent the group to it first
        if obj_parent:
            cmds.parent(zero_grp, obj_parent[0])
            
        # Parent the object under the zero group
        cmds.parent(obj, zero_grp)
        print(f"Created zero group for {obj}")

create_zero_group()
