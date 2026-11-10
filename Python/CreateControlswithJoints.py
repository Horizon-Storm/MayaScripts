import maya.cmds as cmds

#This script is designed so that it sees how many joints have been selected. 
# Then it grabs the control group and duplicates it moving it to the position of the joint. 
# It keeps going until all joints have a control that has had its rotation and translation matched to the joint. 
# It also renames the control to match the name of the joint.

# Read the current selection and separate joints from transform groups.
selection = cmds.ls(selection=True, long=True) or []
joints = [item for item in selection if cmds.nodeType(item) == "joint"]
template_groups = [
    item for item in selection if cmds.nodeType(item) == "transform"
]

# Require at least one joint to create controls for.
if not joints:
    cmds.error("Select one or more joints and a template control group.")

# Require exactly one selected transform to use as the duplication template.
if len(template_groups) != 1:
    cmds.error("Select exactly one template control group along with the joints.")

template_group = template_groups[0]

# Find the NURBS curve shapes inside the template and collect their parent transforms.
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

# Ensure the template contains one control transform, so the duplicate can be renamed.
if len(template_curve_transforms) != 1:
    cmds.error("The template group must contain exactly one NURBS curve control.")

# Create one copy of the template group for every selected joint.
for joint in joints:
    # Use the joint's short name and replace "Jnt" with "Ctrl" for the control name.
    joint_name = joint.rsplit("|", 1)[-1]
    control_name = joint_name.replace("Jnt", "Ctrl")
    group_name = control_name + "_Grp"

    # Get the joint's world-space transformation matrix (position and orientation).
    joint_matrix = cmds.xform(
        joint,
        query=True,
        matrix=True,
        worldSpace=True,
    )

    # Duplicate the template group and give the new group its corresponding name.
    duplicate_group = cmds.duplicate(
        template_group,
        name=group_name,
        renameChildren=True,
        returnRootsOnly=True,
    )[0]

    # Match the duplicate group's world-space transform to the joint.
    cmds.xform(duplicate_group, matrix=joint_matrix, worldSpace=True)

    # Find the duplicated control curve's transform and rename it for this joint.
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
