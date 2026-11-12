import maya.cmds as cmds

#TO USE:
# Select one or more joints and one group containing a NURBS curve control template.
# Run the script and choose FK or IK controls in the first prompt.
# FK controls match joint position and rotation; IK controls match position only.
# Choose Yes in the second prompt to color controls: FK is blue (6), IK is red (13).
# Choose No to keep the template color, or recolor the controls later with ControlColoringScript.py.
# Check the created controls before adding them to the hierarchy.



# Create one control per selected joint. match_rotation selects full-transform (FK)
# versus translation-only (IK) matching; override_color=None leaves template colors unchanged.
def create_controls(match_rotation, override_color):
    # Read the selection and separate joints from the control-group transform.
    selection = cmds.ls(selection=True, long=True) or []
    joints = [item for item in selection if cmds.nodeType(item) == "joint"]
    template_groups = [
        item for item in selection if cmds.nodeType(item) == "transform"
    ]

    # Stop unless at least one joint was selected.
    if not joints:
        cmds.error("Select one or more joints and a template control group.")

    # Stop unless exactly one transform was selected as the duplication template.
    if len(template_groups) != 1:
        cmds.error("Select exactly one template control group along with the joints.")

    template_group = template_groups[0]

    # Find the template's NURBS curve shapes and their parent control transforms.
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

    # Require one control transform so each duplicate has a single control to rename.
    if len(template_curve_transforms) != 1:
        cmds.error("The template group must contain exactly one NURBS curve control.")

    # Duplicate and position the template once for each selected joint.
    for joint in joints:
        # Build control and group names from the joint name (Jnt becomes Ctrl).
        joint_name = joint.rsplit("|", 1)[-1]
        control_name = joint_name.replace("Jnt", "Ctrl")
        group_name = control_name + "_Grp"

        # FK reads the full world matrix; IK reads only world translation.
        if match_rotation:
            joint_transform = cmds.xform(
                joint,
                query=True,
                matrix=True,
                worldSpace=True,
            )
        else:
            joint_transform = cmds.xform(
                joint,
                query=True,
                translation=True,
                worldSpace=True,
            )

        # Duplicate the template group using the name generated for this joint.
        duplicate_group = cmds.duplicate(
            template_group,
            name=group_name,
            renameChildren=True,
            returnRootsOnly=True,
        )[0]

        # Apply the full FK matrix or only IK translation, preserving IK rotation.
        if match_rotation:
            cmds.xform(duplicate_group, matrix=joint_transform, worldSpace=True)
        else:
            cmds.xform(
                duplicate_group,
                translation=joint_transform,
                worldSpace=True,
            )

        # Find the duplicated curve transform and rename it to match the joint.
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
        renamed_control = cmds.rename(duplicate_curve, control_name)

        # Override the curve shape colors only when the user chose to color controls.
        if override_color is not None:
            control_shapes = cmds.listRelatives(
                renamed_control,
                children=True,
                shapes=True,
            ) or []
            for shape in control_shapes:
                # Enable drawing overrides, then apply Maya's indexed color value.
                cmds.setAttr("%s.overrideEnabled" % shape, 1)
                cmds.setAttr("%s.overrideColor" % shape, override_color)


# FK controls match each joint's complete world transform and use blue when colored.
def create_fk_controls(override_color):
    create_controls(match_rotation=True, override_color=override_color)


# IK controls match each joint's world position and use red when colored.
def create_ik_controls(override_color):
    create_controls(match_rotation=False, override_color=override_color)


# Ask which control type to create; canceling or dismissing the prompt creates nothing.
control_type = cmds.confirmDialog(
    title="Create Controls",
    message="Which controls would you like to create?",
    button=["FK Controls", "IK Controls", "Cancel"],
    defaultButton="FK Controls",
    cancelButton="Cancel",
    dismissString="Cancel",
)

if control_type in ("FK Controls", "IK Controls"):
    # Ask whether to apply the mode's color override; No keeps template colors.
    color_controls = cmds.confirmDialog(
        title="Color Controls",
        message="Do you want your controls colored?",
        button=["Yes", "No"],
        defaultButton="Yes",
        cancelButton="No",
        dismissString="No",
    )
    override_color = None
    if color_controls == "Yes":
        # Maya indexed color 6 is blue and 13 is red.
        override_color = 6 if control_type == "FK Controls" else 13

    # Run the selected creation workflow with the user's color preference.
    if control_type == "FK Controls":
        create_fk_controls(override_color)
    else:
        create_ik_controls(override_color)
