# tkAddStitchLocs.py
# mar 2021
# Thomas Kutschera
# add locators

import maya.cmds as cmds
import maya.mel as mel

if cmds.objExists('global_C0_ctl') and cmds.objExists('global_C1_ctl') and cmds.objExists('local_C1_ctl') and cmds.objExists('cog_C1_ctl'): 
    gloPH = cmds.spaceLocator(p=(0, 0, 0), n=('global_C_001_CTRL_PH'))
    gloSN = cmds.spaceLocator(p=(0, 0, 0), n=('global_C_001_CTRL_SN'))
    locPH = cmds.spaceLocator(p=(0, 0, 0), n=('local_C_001_CTRL_PH'))
    locSN = cmds.spaceLocator(p=(0, 0, 0), n=('local_C_001_CTRL_SN'))
    cogPH = cmds.spaceLocator(p=(0, 0, 0), n=('cog_C_001_CTRL_PH'))
    cogSN = cmds.spaceLocator(p=(0, 0, 0), n=('cog_C_001_CTRL_SN'))
    
    cmds.parent(gloSN, gloPH)       
    cmds.parent(locSN, locPH)       
    cmds.parent(cogSN, cogPH)
    
    cmds.parent(gloPH, 'global_C1_ik_cns')
    cmds.parent(locPH, 'local_C1_ik_cns')
    cmds.parent(cogPH, 'cog_C1_ik_cns')

    cmds.parent('global_C1_ctl', gloSN)
    cmds.parent('local_C1_ctl', locSN)
    cmds.parent('cog_C1_ctl', cogSN)
    
    if cmds.objExists('global_C0_ctl'):
        print ('renaming')
        cmds.rename('global_C0_ctl', 'world_C1_ctl')
     
    print ('done successfully :)')

else:
    print ('missing elements :(')
    