import maya.cmds as cmds
  
sels = cmds.ls(sl=True)
for sel in sels:
    if cmds.nodeType(sel) == "joint" or cmds.objectType(sel, isAType="shape"):
        shapes = [sel]
    else:
        shapes = cmds.listRelatives(sel, children=True, shapes=True) or []

    for shape in shapes:
        cmds.setAttr("%s.overrideEnabled" % (shape), 1)
        cmds.setAttr("%s.overrideColor" % (shape), 14)  # Change the number to the desired color index (0-31)

        #Set Specific Color Value
        #cmds.setAttr("%s.overrideColor" % (shape), r, g, b)  # r, g, b values are between 0-1
        #to use comment out the other override color and uncomment the line above with the values.


#0 is off
#1 is Black
#2 is Dark Grey
#3 is Light Grey
#4 is Dark Red
#5 is Dark Blue/Navy
#6 is Blue - FK Controls
#7 is Dark Green
#8 is Dark Purple
#9 is Pink (Hand Controls)
#10 is Brown
#11 is Dark Brown
#12 is Red Brown
#13 is Red - IK Controls
#14 is Green - RK Controls
#15 is Dark Teal Blue
#16 is White (Facial Controls)
#17 is Yellow COG Controls
#18 is Light Blue/Cyan
#19 is Light Green/Mint
#20 is Peach
#21 is Brown Grey/Tan
#22 is Pale Yellow
#23 is Pale Green
#24 is Skin Tone
#25 is Pale Gold
#26 is Olive
#27 is Pale Cyan
#28 is Pale Teal
#29 is Pale Blue
#30 is Pale Purple
#31 is Pale Pink