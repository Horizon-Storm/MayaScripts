
##Copy the springAngleBias ramp from one Maya object to multiple objects.

##How to use:
##1. In Maya, select the source object first.
##2. Select one or more destination objects after it.
##3. Run this script from the Python tab in Maya's Script Editor.

##For each destination, this replaces its existing ramp points with the source
##positions, values, and interpolation settings. Destination ramp fields are
##unlocked and incoming connections are disconnected as needed. Point 0's
##position is then set to 0 and locked.

##This modifies destination objects and may remove their existing connections;
##save a scene copy first if you need to preserve the original setup.


import maya.cmds as cmds


# Ramp attribute and child fields that are copied from source to destination.
RAMP_ATTR = "springAngleBias"
RAMP_FIELDS = (
    "springAngleBias_Position",
    "springAngleBias_FloatValue",
    "springAngleBias_Interp",
)


def unlock_and_disconnect(attr):
    """Make a destination ramp field writable before replacing its value."""
    if not cmds.objExists(attr):
        raise RuntimeError(f"Attribute does not exist: {attr}")

    if cmds.getAttr(attr, lock=True):
        cmds.setAttr(attr, lock=False)

    # Only incoming connections prevent this attribute from being set.
    for source_plug in cmds.listConnections(
        attr, source=True, destination=False, plugs=True
    ) or []:
        cmds.disconnectAttr(source_plug, attr)


def clear_ramp_points(node):
    """Remove existing destination ramp points other than point 0."""
    ramp = f"{node}.{RAMP_ATTR}"
    indices = cmds.getAttr(ramp, multiIndices=True) or []

    for index in reversed(indices):
        if index == 0:
            continue

        for field in RAMP_FIELDS:
            unlock_and_disconnect(f"{ramp}[{index}].{field}")

        cmds.removeMultiInstance(f"{ramp}[{index}]", b=True)


def copy_ramp(destination, ramp_values):
    """Replace one destination ramp with values read from the source."""
    if not cmds.objExists(f"{destination}.{RAMP_ATTR}"):
        print(f"Skipping {destination}: it has no {RAMP_ATTR} attribute.")
        return

    clear_ramp_points(destination)

    for index, (position, value, interpolation) in enumerate(ramp_values):
        values = (position, value, interpolation)
        for field, field_value in zip(RAMP_FIELDS, values):
            attr = f"{destination}.{RAMP_ATTR}[{index}].{field}"
            unlock_and_disconnect(attr)
            cmds.setAttr(attr, field_value)

    # Keep point 0 fixed at the start of the destination ramp.
    position_attr = f"{destination}.{RAMP_ATTR}[0].springAngleBias_Position"
    unlock_and_disconnect(position_attr)
    try:
        cmds.setAttr(position_attr, 0)
    finally:
        cmds.setAttr(position_attr, lock=True)


selection = cmds.ls(selection=True) or []
if len(selection) < 2:
    print("Select a source first, then one or more destination objects.")
else:
    # Maya's selection order determines the source and destination objects.
    source = selection[0]
    destinations = selection[1:]
    source_ramp = f"{source}.{RAMP_ATTR}"

    if not cmds.objExists(source_ramp):
        print(f"{source} does not have a {RAMP_ATTR} attribute.")
    else:
        # Read all source values before changing any destination ramps.
        source_indices = cmds.getAttr(source_ramp, multiIndices=True) or []
        ramp_values = []
        for index in source_indices:
            ramp_values.append(
                (
                    cmds.getAttr(
                        f"{source_ramp}[{index}].springAngleBias_Position"
                    ),
                    cmds.getAttr(
                        f"{source_ramp}[{index}].springAngleBias_FloatValue"
                    ),
                    cmds.getAttr(
                        f"{source_ramp}[{index}].springAngleBias_Interp"
                    ),
                )
            )

        # Apply the captured source ramp to each selected destination.
        for destination in destinations:
            if destination == source:
                continue
            try:
                copy_ramp(destination, ramp_values)
                print(f"Copied {RAMP_ATTR} from {source} to {destination}.")
            except RuntimeError as error:
                print(f"Failed to copy to {destination}: {error}")
