# Set selected objects' translation and rotation values below 0.001 to zero.
# Also check joint-orient values on selected joints.

import maya.cmds as cmds


def zero_small_values():
    # Get the selected objects using their full scene paths.
    selection = cmds.ls(selection=True, objectsOnly=True, long=True) or []
    if not selection:
        cmds.warning("Select one or more objects first.")
        return

    # Values with an absolute magnitude below this threshold will be zeroed.
    threshold = 0.001

    # Translation and rotation attributes available on transform objects.
    transform_attrs = (
        "translateX", "translateY", "translateZ",
        "rotateX", "rotateY", "rotateZ",
    )

    # Joint orientation attributes; other objects will be skipped if they lack them.
    joint_attrs = ("jointOrientX", "jointOrientY", "jointOrientZ")

    # Check each selected object's transform and joint-orient attributes.
    for obj in selection:
        for attr in transform_attrs + joint_attrs:
            # Skip attributes that do not exist on this object.
            if not cmds.attributeQuery(attr, node=obj, exists=True):
                continue

            # Set the attribute to zero only when its value is close to zero.
            plug = "{}.{}".format(obj, attr)
            if abs(cmds.getAttr(plug)) < threshold:
                cmds.setAttr(plug, 0)


# Run the cleanup when this script is executed.
zero_small_values()