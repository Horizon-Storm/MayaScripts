#this is to select a group of joints and auto set their preferred angle to a specific number
#select the joints
#open Dialoge box showing X Y Z asking what you want the preffered angle to be
#set all their preffered angle to whatever the user inputs.

import maya.cmds as cmds


def show_preferred_angle_dialog():
    # Collect selected joints; the long names avoid ambiguity in nested hierarchies.
    joints = cmds.ls(selection=True, type="joint", long=True) or []
    if not joints:
        # Stop and notify the user if there are no selected joints.
        cmds.warning("Select one or more joints before running this script.")
        return

    # Read Maya's current angle unit so the dialog can label the values clearly.
    angle_unit = cmds.currentUnit(query=True, angle=True)
    window_name = "setPreferredAnglesWindow"

    # Remove an existing copy of this dialog before creating a new one.
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    # Create the dialog window and its main vertical layout.
    window = cmds.window(
        window_name,
        title="Set Joint Preferred Angles",
        sizeable=False,
    )
    cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=8,
        columnOffset=("both", 10),
    )
    # Show how many joints will be changed and which angle unit is in use.
    cmds.text(
        label="Enter preferred angles for {} joint(s) ({})".format(
            len(joints), angle_unit
        )
    )

    # Create one numeric input field for each preferred-angle axis.
    fields = {}
    for axis in ("X", "Y", "Z"):
        cmds.rowLayout(
            numberOfColumns=2,
            adjustableColumn=2,
            columnWidth2=(30, 120),
        )
        cmds.text(label=axis)
        fields[axis] = cmds.floatField(value=0.0, precision=3)
        cmds.setParent("..")

    # Read the entered values and apply each one to every selected joint.
    def apply_angles(*_):
        values = {
            axis: cmds.floatField(field, query=True, value=True)
            for axis, field in fields.items()
        }

        for joint in joints:
            for axis, value in values.items():
                cmds.setAttr(
                    "{}.preferredAngle{}".format(joint, axis),
                    value,
                )

        # Close the dialog once the new values have been applied.
        cmds.deleteUI(window)

    # Add buttons to apply the values or close the dialog without changing them.
    cmds.rowLayout(
        numberOfColumns=2,
        columnWidth2=(80, 80),
        columnAlign2=("center", "center"),
    )
    cmds.button(label="Apply", command=apply_angles)
    cmds.button(
        label="Cancel",
        command=lambda *_: cmds.deleteUI(window),
    )

    # Display the completed dialog.
    cmds.showWindow(window)


# Open the preferred-angle dialog when this script runs.
show_preferred_angle_dialog()