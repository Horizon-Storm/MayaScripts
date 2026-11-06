#Batch Renamer, select the object to clean up teh name and correct hte suffix.

import maya.cmds as cmds

def add_suffix_to_selection():
    """Adds appropriate suffixes to selected objects based on their type."""
    selection = cmds.ls(selection=True)
    
    if not selection:
        cmds.warning("Please select at least one object.")
        return

    for obj in selection:
        # Check if the object already has a common suffix
        if any(suffix in obj for suffix in ['_geo', '_jnt', '_ctrl', '_grp']):
            continue
            
        obj_type = cmds.objectType(obj)
        suffix = ""
        
        if obj_type == 'transform':
            # Check the shape node underneath
            shapes = cmds.listRelatives(obj, shapes=True)
            if shapes and cmds.objectType(shapes[0]) == 'mesh':
                suffix = "_geo"
            else:
                suffix = "_grp"
        elif obj_type == 'joint':
            suffix = "_jnt"
            
        if suffix:
            new_name = f"{obj}{suffix}"
            cmds.rename(obj, new_name)
            print(f"Renamed {obj} to {new_name}")

add_suffix_to_selection()
