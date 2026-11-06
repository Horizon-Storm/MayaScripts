import maya.cmds as cmds

selected_objects = cmds.ls(selection=True)
if not selected_objects:
    raise RuntimeError("Select at least one object.")

#sets events for the rotation of selected objects
attributes = ("rotateX", "rotateY", "rotateZ")
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



for obj in selected_objects:
    for frame, rotation in events:
        for attr, value in zip(attributes, rotation):
            cmds.setKeyframe(obj, attribute=attr, value=value, time=frame)

attributes = ("translateX", "translateY", "translateZ")
#sets events after frame 90 to stretch it once on X
events_after_90 = [
    (90, (0, 0, 0)),
    (100, (0, 2, 0)),
    (110, (0, 0, 0)),
]

for obj in selected_objects:
    for frame, translation in events_after_90:
        for attr, value in zip(attributes, translation):
            cmds.setKeyframe(obj, attribute=attr, value=value, time=frame)