import maya.cmds as cmds

#get a list of everything of a specific type (joint)
joints = cmds.ls(type='joint')

#turn off scale compensate value for all joints
for x in joints:
    cmds.setAttr('%s.segmentScaleCompensate' % (x), 0)
