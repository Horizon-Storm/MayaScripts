import maya.cmds as cmds

# Get the selected objects and stop with an error if nothing is selected.
selected_objects = cmds.ls(selection=True)
if not selected_objects:
    raise RuntimeError("Select at least one object.")

#sets events for the rotation of selected objects
# These are the three rotation channels that will receive animation keys.
attributes = ("rotateX", "rotateY", "rotateZ")
# Each tuple contains a frame number and the X, Y, and Z rotation values at that frame.
events = [
    (0,  (0,   0,   0)),
    (10, (20,  0,   0)),
    (20, (-20, 0,   0)),
    (30, (0,   0,   0)),
    (40, (0,  20,   0)),
    (50, (0, -20,   0)),
    (60, (0,   0,   0)),
    (70, (0,   0,  20)),
    (80, (0,   0, -20)),
    (90, (0,   0,   0)),
]


# Add each rotation key to every selected object.
for obj in selected_objects:
    # Apply each frame's rotation values to their matching rotation channels.
    for frame, rotation in events:
        for attr, value in zip(attributes, rotation):
            cmds.setKeyframe(obj, attribute=attr, value=value, time=frame)

# Switch to the translation channels for the additional animation section.
attributes = ("translateX", "translateY", "translateZ")
#sets events after frame 90 to stretch it once on X
# Each tuple contains a frame number and X, Y, and Z translation values.
# Note: these values change translateY at frame 100, not translateX.
events_after_90 = [
    (90, (0, 0, 0)),
    (100, (0, 2, 0)),
    (110, (0, 0, 0)),
]

# Add the translation keys to every selected object.
for obj in selected_objects:
    # Apply each frame's translation values to their matching translation channels.
    for frame, translation in events_after_90:
        for attr, value in zip(attributes, translation):
            cmds.setKeyframe(obj, attribute=attr, value=value, time=frame)