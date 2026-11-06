import maya.cmds as cmds

# Method that gets selected objects;
def get_selected_objects():
    selected_objects = cmds.ls(selection=True)

    # For each object in the selection create an empty group
    for obj in selected_objects:
        group = cmds.group(empty=True, name=obj +"_Grp")

        # Get the Matrix of the object and move the group to that position
        crntposition = cmds.xform(obj, query=True, matrix=True, worldSpace=True)
        cmds.xform(group, matrix=crntposition, worldSpace=True)

        # Parent the object under the group
        cmds.parent(obj, group)

# Run the method
get_selected_objects()