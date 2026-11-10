# Add a suffix to selected Maya objects based on their type.

import maya.cmds as cmds


def add_suffix_to_selection():
    """Adds appropriate suffixes to selected objects based on their type."""
    # Get the objects currently selected in Maya.
    selection = cmds.ls(selection=True)

    # Stop and display a warning if nothing is selected.
    if not selection:
        cmds.warning("Please select at least one object.")
        return

    # Check each selected object and determine which suffix it needs.
    for obj in selection:
        # Leave objects alone if their name already contains a recognized suffix.
        if any(suffix in obj for suffix in ['_geo', '_jnt', '_ctrl', '_grp']):
            continue

        # Find the Maya node type so the appropriate suffix can be chosen.
        obj_type = cmds.objectType(obj)
        suffix = ""

        if obj_type == 'transform':
            # Inspect the object's shape to distinguish geometry from a group.
            shapes = cmds.listRelatives(obj, shapes=True)
            if shapes and cmds.objectType(shapes[0]) == 'mesh':
                suffix = "_geo"
            else:
                suffix = "_grp"
        elif obj_type == 'joint':
            suffix = "_jnt"

        # Rename the object only when a suffix was selected for its type.
        if suffix:
            new_name = f"{obj}{suffix}"
            cmds.rename(obj, new_name)
            print(f"Renamed {obj} to {new_name}")


# Run the renamer when this script is executed.
add_suffix_to_selection()
