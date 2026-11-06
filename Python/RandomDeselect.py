#This simple script just randomly selects a percentage of the objects in your current selection - very useful for quickly creating randomness.  

import maya.cmds as cmds
import random

keep = 0.5;
        
# save selection as a list, create empty list
sel = cmds.ls(sl=1)
new_sel = []
        
# iterate over list only keeping some objects
for item in sel:
    print item
    if random.random() < keep:
        new_sel.append(item)
                
# select new selection
cmds.select(new_sel)