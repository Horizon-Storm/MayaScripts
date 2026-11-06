#Random Deselect Tool, Randomly drops a percentage of currently selected objects in Maya.

import maya.cmds as cmds
import random

def random_deselect(percentage=50):
    """Randomly deselects a percentage of the currently selected objects."""
    selection = cmds.ls(selection=True)
    if not selection:
        cmds.warning("Nothing selected.")
        return
        
    # Calculate how many items to remove
    num_to_deselect = int(len(selection) * (percentage / 100.0))
    
    # Randomly pick items to drop
    to_deselect = random.sample(selection, num_to_deselect)
    
    # Remove them from the active Maya selection
    cmds.select(to_deselect, deselect=True)
    print(f"Deselected {num_to_deselect} objects.")

# Change the number to adjust what percentage of objects to deselect
random_deselect(percentage=40)
