# tkStitchheadHelper.py

import functools as partial
import maya.cmds as cmds
import maya.mel as mel

def cImportGuides(*args):
    # cmd1 = 'file -import -type "mayaAscii"  -ignoreVersion -mergeNamespacesOnClash false -rpr "_guides" -options "v=0;"  -pr  -importFrameRate true  -importTimeRange "override" "X:/stitchhead_shd-5070/_sandbox/thomas.kutschera/assets/_guides.ma"'
    cmd1 = 'file -import -type "mayaAscii" -ignoreVersion -mergeNamespacesOnClash false -rpr "_guides" -options "v=0;"  -pr  -importFrameRate true -importTimeRange "override" "C:/gitRepository/tkStitchHead/_guides.ma"'
    mel.eval(cmd1)
    
    
def cAddStitchLocs(*args):
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
    
    
def cFindEmptyTransforms(*args):
    dags = cmds.ls(l=1, type='transform')
    for dag in dags:
        shps = cmds.listRelatives(dag, s=1)
        if shps == 'None':
            ending = dag.split('_')[-1]
            if ending != 'GRUP':
                cmds.select(dag, r=1)
                print 'ending: ' + ending
                cmd1 = 'searchReplaceNames("'
                cmd2 = '", "'
                cmd3 = '", "selected")'
                cmd = cmd1 + ending + cmd2 + 'GRUP' + cmd3
                print cmd
                mel.eval(cmd)
        # else:
            # print 'has shapes'


def cAddAttributes(*args):
    carries = ['world_C_001_CTRL', 'global_C_001_CTRL',  'local_C_001_CTRL']
    carryWorld = carries[0]
    carryGlobal = carries[1]
    carryLocal = carries[2]
    geoGrp = 'geo_C_001_GRUP'
    ctlGrp = 'cogRoot_C_001_GRUP'
    gloSclMult =  cmds.shadingNode('multiplyDivide', asUtility=1, n='globalScaleOverride_C_001_RMDI')
    
    # create nodes
    # cmds.shadingNode('multiplyDivide', asUtility=1, n=gloSclMult)
    
    cmds.setAttr(gloSclMult + '.input2X', 1)
    cmds.setAttr(gloSclMult + '.input2Y', 1)
    cmds.setAttr(gloSclMult + '.input2Z', 1)
    cmds.setAttr(gloSclMult + '.operation', 1)

    
    # add attributes
    for carry in carries:
        print carry
        print 'world'
        cmds.addAttr(carry, sn='_', ln='___________', at='enum', en='GLOBAL')
        cmds.setAttr(carry + '._', e=1,  k=0, cb=1)
        
        print 'global scale'
        cmds.addAttr(carry, ln='globalScale', at='double', dv=1, min=.1) 
        cmds.setAttr(carry + '.globalScale', e=1, keyable=1)
        
        print 'display'
        cmds.addAttr(carry, sn='__', ln='____________', at='enum', en='DISPLAY')
        cmds.setAttr(carry + '.__', e=1,  k=0, cb=1)
        
        print 'ctrl display'
        cmds.addAttr(carry, ln='ctrlDisplay', at='bool', dv=1, min=.1) 
        cmds.setAttr(carry + '.ctrlDisplay', e=1, keyable=1)
        
        cmds.addAttr(carry, ln='ctrlHideOnPlay', at='bool', dv=1, min=.1) 
        cmds.setAttr(carry + '.ctrlHideOnPlay', e=1, keyable=1)
        
        cmds.addAttr(carry, ln='geoDisplay', at='bool', dv=1, min=.1) 
        cmds.setAttr(carry + '.geoDisplay', e=1, keyable=1)

        cmds.addAttr(carry, ln='geoReference', at='bool', dv=1, min=.1) 
        cmds.setAttr(carry + '.geoReference', e=1, keyable=1)
        
        cmds.connectAttr(gloSclMult + '.outputX', carry + '.scaleX', f=1)
        cmds.connectAttr(gloSclMult + '.outputY', carry + '.scaleY', f=1)
        cmds.connectAttr(gloSclMult + '.outputZ', carry + '.scaleZ', f=1)
        
        
    # connect attributes
    cmds.connectAttr(carryLocal + '.scaleX', gloSclMult + '.input1.input1X', f=1)
    cmds.connectAttr(carryLocal + '.scaleY', gloSclMult + '.input1.input1Y', f=1)
    cmds.connectAttr(carryLocal + '.scaleZ', gloSclMult + '.input1.input1Z', f=1)
    cmds.setAttr (geoGrp + '.overrideEnabled', 1)
    cmds.connectAttr(carryLocal + '.ctrlDisplay', ctlGrp + '.visibility', f=1)
    cmds.connectAttr(carryLocal + '.ctrlHideOnPlay', ctlGrp + '.hideOnPlayback', f=1)
    cmds.connectAttr(carryLocal + '.geoDisplay', geoGrp + '.visibility', f=1)
    cmds.connectAttr(carryLocal + '.geoReference', geoGrp + '.geoReference', f=1)
    
    
    # lock attributes
    cmds.setAttr(gloSclMult + 'i2', lock=1)
    cmds.setAttr(gloSclMult + 'i1', lock=1)


def cRenameNodes(*args):
    nameList = [
    'grp', 'GRUP', 'GRP', 'GRUP', 'ctl', 'CTRL', 'CON', 'CTRL', 'JNT', 'JOIN', 'jnt', 'JOIN', 
    'parentConstraint1', 'DPAR', 'scaleConstrainta', 'DSCC', 'pointConstraint1', 'DPCC', 'orientConstraint1', 
    'DOCC', 'root', 'ROOT', '_C1_ik_cns', 'IkCns_C_001_GRUP', '_C1_root', 'Root_C_001_GRUP', 
    '_C1', '_C_001', '_L1', '_L_001', '_R1', '_R_001',
    ]
    
    for i in range(0,len(nameList), 2):
        cmd1 = 'searchReplaceNames("'
        cmd2 = '", "'
        cmd3 = '", "all")'
        cmd = cmd1 + nameList[i] + cmd2 + nameList[i+1] + cmd3
        print cmd
        mel.eval(cmd)
        


''' window '''
ver = 'v0.1';
windowStartHeight = 50;
windowStartWidth = 450;
bh1 = 18;
bh2 = 22;

if cmds.window('win_tkStitchheadHelper', exists=1):
	cmds.deleteUI('win_tkStitchheadHelper')

myWindow = cmds.window('win_tkStitchheadHelper', t=('xGen Helper ' + ver), s=1, wh=(windowStartHeight, windowStartWidth ))
cmds.columnLayout(adj=1, bgc=(0,0,0))
cmds.button(l='1. Import Guides', c=cImportGuides)
cmds.button(l='1. Add Special Locs', c=cAddStitchLocs)
cmds.button(l='3. Rename Nodes', c=cRenameNodes)
cmds.button(l='4. Add Attributes', c=cAddAttributes)
cmds.button(l='5. Add GRUP', c=cFindEmptyTransforms)

cmds.showWindow(myWindow)

cmds.window(myWindow, w=300, h=100, e=1)
