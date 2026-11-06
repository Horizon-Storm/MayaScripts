import maya.cmds as cmds

#make viewport selection, parent controls, and then child controls


#get selection, seperate parent controls and child controls
sels = cmds.ls(sl=True) #[parent control, child control]
parent_ctrl = sels[0]
child_ctrl = sels[1]

#get the parent group of the child control
child_ctrl_grp = cmds.listRelatives(child_ctrl, parent=True)[0] #[child controls parent node]

#create constraints
p_constraintt = cmds.parentConstraint(parent_ctrl, child_ctrl_grp, mo=True, skipRotate = ['x', 'y', 'z'], weight=1) #constrain translates
p_constraintr = cmds.parentConstraint(parent_ctrl, child_ctrl_grp, mo=True, skipTranslate = ['x', 'y', 'z'], weight=1) #constrain rotates
cmds.scaleConstraint(parent_ctrl, child_ctrl_grp, weight=1) #constrain scale

#check if attribute already exists on the child control, if it does delete it
if cmds.attributeQuery('FollowTranslate', node=child_ctrl, exists=True):
    cmds.deleteAttr('%s.FollowTranslate' % (child_ctrl))
    
if cmds.attributeQuery('FollowRotate', node=child_ctrl, exists=True):
    cmds.deleteAttr('%s.FollowRotate' % (child_ctrl))


#create attributes on the child control
cmds.addAttr(child_ctrl, ln='FollowTranslate', at='double', min=0, max=1, dv=1)
cmds.setAttr('%s.FollowTranslate' % (child_ctrl), e=True, keyable=True)
cmds.addAttr(child_ctrl, ln='FollowRotate', at='double', min=0, max=1, dv=1)
cmds.setAttr('%s.FollowRotate' % (child_ctrl), e=True, keyable=True)


#connect the attributes from the child control to constraint weights
cmds.connectAttr('%s.FollowTranslate' % (child_ctrl), '%s.w0' % (p_constraintt[0]), f=True)
cmds.connectAttr('%s.FollowRotate' % (child_ctrl), '%s.w0' % (p_constraintr[0]), f=True)