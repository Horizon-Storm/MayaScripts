import maya.cmds as cmds

#This script is designed so that it sees how many joints have been selected. 
# Then it grabs the control group and duplicates it moving it to the position of the joint. 
# It keeps going until all joints have a control that has had its rotation and translation matched to the joint. 
# It also renames the control to match the name of the joint.



selection = cmds.ls(selection=True, long=True) or []
joints = [item for item in selection if cmds.nodeType(item) == "joint"]
template_groups = [
    item for item in selection if cmds.nodeType(item) == "transform"
]

if not joints:
    cmds.error("Select one or more joints and a template control group.")

if len(template_groups) != 1:
    cmds.error("Select exactly one template control group along with the joints.")

template_group = template_groups[0]

template_curves = cmds.listRelatives(
    template_group,
    allDescendents=True,
    type="nurbsCurve",
    fullPath=True,
) or []
template_curve_transforms = {
    cmds.listRelatives(curve, parent=True, fullPath=True)[0]
    for curve in template_curves
}

if len(template_curve_transforms) != 1:
    cmds.error("The template group must contain exactly one NURBS curve control.")

for joint in joints:
    joint_name = joint.rsplit("|", 1)[-1]
    control_name = joint_name.replace("Jnt", "Ctrl")
    group_name = control_name + "_Grp"
    joint_matrix = cmds.xform(
        joint,
        query=True,
        matrix=True,
        worldSpace=True,
    )
    duplicate_group = cmds.duplicate(
        template_group,
        name=group_name,
        renameChildren=True,
        returnRootsOnly=True,
    )[0]
    cmds.xform(duplicate_group, matrix=joint_matrix, worldSpace=True)

    duplicate_curves = cmds.listRelatives(
        duplicate_group,
        allDescendents=True,
        type="nurbsCurve",
        fullPath=True,
    ) or []
    duplicate_curve = cmds.listRelatives(
        duplicate_curves[0],
        parent=True,
        fullPath=True,
    )[0]
    cmds.rename(duplicate_curve, control_name)
