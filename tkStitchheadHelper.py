# tkStitchheadHelper.py

import functools as partial
import maya.cmds as cmds
import maya.mel as mel

def cImportGuides(*args):
    # cmd1 = 'file -import -type "mayaAscii"  -ignoreVersion -mergeNamespacesOnClash false -rpr "_guides" -options "v=0;"  -pr  -importFrameRate true  -importTimeRange "override" "X:/stitchhead_shd-5070/_sandbox/thomas.kutschera/assets/_guides.ma"'
    cmd1 = 'file -import -type "mayaAscii" -ignoreVersion -mergeNamespacesOnClash false -rpr "_guides" -options "v=0;"  -pr  -importFrameRate true -importTimeRange "override" "C:/gitRepository/tkStitchHead/_guides.ma"'
    mel.eval(cmd1)

    print 'success'

    
    
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

    print 'success'
 
    

def cRenameNodes(*args):
    nameList = [
    'grp', 'GRUP', 'GRP', 'GRUP', 'ctl', 'CTRL', 'CON', 'CTRL', 'JNT', 'JOIN', 'jnt', 'JOIN', 
    'parentConstraint1', 'DPAR', 'scaleConstrainta', 'DSCC', 'pointConstraint1', 'DPCC', 'orientConstraint1', 
    'DOCC', '_C1_ik_cns', 'IkCns_C_001_GRUP', '_C1_root', 'Root_C_001_GRUP', 
    '_C1', '_C_001', '_L1', '_L_001', '_R1', '_R_001',
    ]
    
    for i in range(0,len(nameList), 2):
        cmd1 = 'searchReplaceNames("'
        cmd2 = '", "'
        cmd3 = '", "all")'
        cmd = cmd1 + nameList[i] + cmd2 + nameList[i+1] + cmd3
        print cmd
        mel.eval(cmd)

    print 'success'
        

def cFindEmptyTransforms(*args):
    dagsFound = []
    exception = ['geo_C_001_GRUP', 'rig_C_001_GRUP', 'setup', 'JOIN_org']

    print 'cFindEmptyTransforms'
    dags = cmds.ls(type='transform')
    for dag in dags:
        shps = cmds.listRelatives(dag, s=1)
        if shps:
            pass
        else:
            if dag not in exception:
                print 'GRUP'
                ending = dag.split('_')[-1]
                if ending != 'GRUP':
                    dagsFound.append(dag)
                    dagsFound.append(ending)

    for i in range(0, len(dagsFound), 2): 
        dag = dagsFound[i]
        ending = dagsFound[i+1]
        cmds.select(dag, r=1)
        print 'ending: ' + ending
        cmd1 = 'searchReplaceNames("'
        cmd2 = '", "'
        cmd3 = '", "selected")'
        cmd = cmd1 + ending + cmd2 + 'GRUP' + cmd3
        print cmd
        mel.eval(cmd)

    print 'success'


def cAddAttributes(*args):
    carries = ['world_C_001_CTRL', 'global_C_001_CTRL',  'local_C_001_CTRL']
    carryWorld = carries[0]
    carryGlobal = carries[1]
    carryLocal = carries[2]
    geoGrp = 'geo_C_001_GRUP'
    ctlGrp = 'cogRoot_C_001_GRUP'
    gloSclMult =  cmds.shadingNode('multiplyDivide', asUtility=1, n='globalScaleOverride_C_001_RMDI')
    
    cmds.setAttr(gloSclMult + '.operation', 1)

    
    # add attributes
    for carry in carries:
        cmds.addAttr(carry, sn='_', ln='___________', at='enum', en='GLOBAL')
        cmds.setAttr(carry + '._', e=1,  k=0, cb=1)
        
        cmds.addAttr(carry, ln='globalScale', at='double', dv=1, min=.1) 
        cmds.setAttr(carry + '.globalScale', e=1, keyable=1)
        
        cmds.addAttr(carry, sn='__', ln='____________', at='enum', en='DISPLAY')
        cmds.setAttr(carry + '.__', e=1,  k=0, cb=1)
        
        cmds.addAttr(carry, ln='ctrlDisplay', at='bool', dv=1, min=.1) 
        cmds.setAttr(carry + '.ctrlDisplay', e=1, keyable=1)
        
        cmds.addAttr(carry, ln='ctrlHideOnPlay', at='bool', dv=1, min=.1) 
        cmds.setAttr(carry + '.ctrlHideOnPlay', e=1, keyable=1)
        
        cmds.addAttr(carry, ln='geoDisplay', at='bool', dv=1, min=.1) 
        cmds.setAttr(carry + '.geoDisplay', e=1, keyable=1)

        cmds.addAttr(carry, ln='geoReference', at='bool', dv=1, min=.1) 
        cmds.setAttr(carry + '.geoReference', e=1, keyable=1)
        
        
        
    # connect attributes
    cmds.connectAttr(gloSclMult + '.outputX', carryLocal + '.scaleX', f=1)
    cmds.connectAttr(gloSclMult + '.outputY', carryLocal + '.scaleY', f=1)
    cmds.connectAttr(gloSclMult + '.outputZ', carryLocal + '.scaleZ', f=1)

    cmds.connectAttr(carryLocal + '.globalScale', gloSclMult + '.input2.input2X', f=1)
    cmds.connectAttr(carryLocal + '.globalScale', gloSclMult + '.input2.input2Y', f=1)
    cmds.connectAttr(carryLocal + '.globalScale', gloSclMult + '.input2.input2Z', f=1)


    cmds.setAttr (geoGrp + '.overrideEnabled', 1)
    cmds.connectAttr(carryLocal + '.ctrlDisplay', ctlGrp + '.visibility', f=1)
    cmds.connectAttr(carryLocal + '.ctrlHideOnPlay', ctlGrp + '.hideOnPlayback', f=1)
    cmds.connectAttr(carryLocal + '.geoDisplay', geoGrp + '.visibility', f=1)
    cmds.connectAttr(carryLocal + '.geoReference', geoGrp + '.overrideEnabled', f=1)

    cmds.connectAttr(carryLocal + '.geoReference', carryWorld + '.ctrlDisplay', f=1)
    cmds.connectAttr(carryLocal + '.ctrlHideOnPlay', carryWorld + '.ctrlHideOnPlay', f=1)
    cmds.connectAttr(carryLocal + '.geoDisplay', carryWorld + '.geoDisplay', f=1)
    cmds.connectAttr(carryLocal + '.geoReference', carryWorld + '.geoReference', f=1)
    cmds.connectAttr(carryLocal + '.globalScale', carryWorld + '.globalScale', f=1)

    cmds.connectAttr(carryLocal + '.ctrlDisplay', carryGlobal + '.ctrlDisplay', f=1)
    cmds.connectAttr(carryLocal + '.ctrlHideOnPlay', carryGlobal + '.ctrlHideOnPlay', f=1)
    cmds.connectAttr(carryLocal + '.geoDisplay', carryGlobal + '.geoDisplay', f=1)
    cmds.connectAttr(carryLocal + '.geoReference', carryGlobal + '.geoReference', f=1)
    cmds.connectAttr(carryLocal + '.globalScale', carryGlobal + '.globalScale', f=1)

    
    # lock attributes
    cmds.setAttr(gloSclMult + '.i2', lock=1)
    cmds.setAttr(gloSclMult + '.i1', lock=1)

    print 'success'





''' window '''
ver = 'v0.1';
windowStartHeight = 50;
windowStartWidth = 450;
bh1 = 18;
bh2 = 22;
colRed              = [0.44, 0.2, 0.2];
colGreen            = [0.28, 0.44, 0.28];
colGreen2           = [0.18, 0.30, 0.18];
colDark             = [0.08, 0.09, 0.10];
colDark2            = [0.02, 0.21, 0.22];

if cmds.window('win_tkStitchheadHelper', exists=1):
	cmds.deleteUI('win_tkStitchheadHelper')

myWindow = cmds.window('win_tkStitchheadHelper', t=('xGen Helper ' + ver), s=1, wh=(windowStartHeight, windowStartWidth ))
cmds.columnLayout(adj=1, bgc=(colGreen2[0], colGreen2[1], colGreen2[2]))
cmds.button(l='1. Import Guides', c=cImportGuides)
cmds.button(l='Build Gear Rig', c=cAddStitchLocs, bgc=(colGreen[0], colGreen[1], colGreen[2]))
cmds.button(l='2. Add Special Locs', c=cAddStitchLocs)
cmds.button(l='3. Rename Nodes', c=cRenameNodes, bgc=(colGreen[0], colGreen[1], colGreen[2]))
cmds.button(l='4. Add "GRUP" at the end', c=cFindEmptyTransforms, bgc=(colGreen[0], colGreen[1], colGreen[2]))
cmds.button(l='5. Add Attributes', c=cAddAttributes)

cmds.showWindow(myWindow)

cmds.window(myWindow, w=300, h=100, e=1)
