# tkStitchheadHelper.py

from functools import partial 
import maya.cmds as cmds
import maya.mel as mel

def cShrinkWin(windowToClose, *args):
    cmds.window(windowToClose, e=1, h=20, w=440)


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
    'grp', 'GRUP', 'GRP', 'GRUP', 'ctl', 'CTRL', 'CON', 'CTRL', 'JNT', 'JOIN', 'jnt', 'JOIN'
    ]
    
    for i in range(0,len(nameList), 2):
        cmd1 = 'searchReplaceNames("'
        cmd2 = '", "'
        cmd3 = '", "all")'
        cmd = cmd1 + nameList[i] + cmd2 + nameList[i+1] + cmd3
        print cmd
        mel.eval(cmd)

    print 'success'


def cNmSpcCreation(action, *args):
    if action == 'create':
        if cmds.namespace(exists='EX') == 0:
            cmds.namespace(add='EX')

        firstSel = cmds.ls(sl=1, l=1)[0]    
        childs = cmds.listRelatives(firstSel, ad=1, f=1)    

        for node in childs:
            shortName = node.split('|')[-1]
            newName = str('EX:' + shortName)
            cmds.rename(node, newName)

        shortName = firstSel.split('|')[-1]
        newName = str('EX:' + shortName)
        cmds.rename(firstSel, newName)


    if action == 'remove':
        if cmds.namespace(exists='EX') == 1:

            firstSel = cmds.ls(sl=1, l=1)[0]
            childs = cmds.listRelatives(firstSel, ad=1, f=1)    

            for node in childs:
                shortName = node.split('|')[-1]
                newName = shortName.replace('EX:', '')

                cmds.rename(node, newName)
            
            shortName = firstSel.split('|')[-1]
            newName = str('EX:' + shortName)
            cmds.rename(firstSel, newName)


    if action == 'delete':
        if cmds.namespace(exists='EX') == 1:
            cmds.namespace(rm='EX')


def cReorganize(type, *args):
    mySel = cmds.ls(sl=1)[0]
    newName = ''
    name_var = str(mySel)  
    
    splits = name_var.split('_')
    length = len(splits)

    if type == 'Last --> Front':
        newName = splits[0]
        cap = str(splits[length-1]).capitalize()
        newName += cap

        for i in range(1, length-1):
            newName += '_'
            newName += splits[i]

        cmds.rename(mySel, newName)


    if type == 'xx_yy --> xxyy':
        for i in range(0, length-2):
            newName += splits[i]
            newName += '_'
        
        newName += splits[-2]
        newName += splits[-1]


        cmds.rename(mySel, newName)


    if type == 'Switch Last':
        for i in range(0, length-2):
            newName += splits[i]
            newName += '_'
        
        newName += splits[-1]
        newName += '_'
        newName += splits[-2]


        cmds.rename(mySel, newName)


    if type == '1 --> 001':
        newName = splits[0]
        newName += '_' + str(splits[1])
        if len(splits[2]) == 2:
            newName += '_0' + str(splits[2])
        if len(splits[2]) == 1:
            newName += '_00' + str(splits[2])

        for i in range(3, length):
            newName += '_'
            newName += splits[i]

        cmds.rename(mySel, newName)


    if type == 'C1 --> C_1':
        newName = splits[0]
        newName += '_' + str(splits[1])[0]
        newName += '_' + str(splits[1])[1:]

        for i in range(2, length):
            newName += '_'
            newName += splits[i]

        cmds.rename(mySel, newName)


    if type == 'Delete Last':
        for i in range(0, length-1):
            newName += splits[i]
            newName += '_'
        
        newName = newName[0:-1]

        cmds.rename(mySel, newName)


    if type == '_GRUP' or type == '_CTRL' or type == '_JOIN':
        newName = str(mySel) 
        newName += str(type)

        cmds.rename(mySel, newName)


def cNamingConvention(type, *args):
    childs = []
    exception = ['geo_C_001_GRUP', 'rig_C_001_GRUP', 'JOIN_org', 'global_C_001_CTRL_PH', 'global_C_001_CTRL_SN', 'local_C_001_CTRL_PH', 'local_C_001_CTRL_SN', 'cog_C_001_CTRL_PH', 'cog_C_001_CTRL_SN', 'setup', 'jnt_org']
    suffix = [
    'Ctl', '_CTRL', 'Crv', '_NCRV', 'Parentconstraint1', '_DPAR', 'Scaleconstraint1', '_DSCC', 'Pointconstraint1', '_DPOC', 'Orientconstraint1', '_DORC', 'Jnt', '_JOIN'
    ]

    # startSel = cmds.select('rig', r=1)
    entry_trs = cmds.ls(sl=1)[0]
    if type == 'hierarchy':
        childs = cmds.listRelatives(entry_trs, ad=1)
    if type == 'selected':
        childs = cmds.ls(sl=1)
    for node in childs:
        newName = ''
        name_var = str(node)
        splits = name_var.split('_')
        # print splits
        max = len(splits)
        if max > 2:
            newName = str(splits[0])
            for i in range(2, max):
                newName += str(splits[i]).capitalize()

            newName += '_'
            newName += str(splits[1][0])

            length = len(splits[1])

            if length == 2:
                newName += '_00'
                newName += str(splits[1][1])

            if length == 3:
                newName += '_0'
                newName += str(splits[1][1:2])

            if length == 4:
                newName += '_'
                newName += str(splits[1][1:3])

            for k in range(0, len(suffix), 2):
                if suffix[k] in newName:
                    newName = newName.replace(str(suffix[k]),'')
                    newName += str(suffix[k+1])

        shps = cmds.listRelatives(node, s=1)

        if shps or cmds.objectType(node, isType='ikEffector') or cmds.objectType(node, isType='joint') or cmds.objectType(node, isType='parentConstraint') or cmds.objectType(node, isType='pointConstraint') or cmds.objectType(node, isType='orientConstraint') or cmds.objectType(node, isType='scaleConstraint'):
            pass
            
        else:
            if node not in exception:
                newName += '_GRUP'

        print newName
        print str(node) + ' --> ' + str(newName)
        new = str(newName)
        if len(new) != 0:
            cmds.rename(node, newName)
        

def cCheckConstraints(*args):
    objTypes = ['parentConstraint', 'DPAR', 'scaleConstraint', 'DSCC', 'pointConstraint', 'DPOC', 'orientConstraint', 'DORC']

    for i in range(0, len(objTypes), 2):
        pars = cmds.ls(type=objTypes[i])
        for ps in pars:
            newName = ''
            syllables = ps.split('_')
            for j in range(0, len(syllables)-1):
                newName += syllables[j] + '_'
            newName += str(objTypes[i+1])
            print newName
            cmds.rename(ps, newName)


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

    print dagsFound

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
windowStartHeight = 150;
windowStartWidth = 440;
bh1 = 18;
bh2 = 22;
colRed              = [0.44, 0.2, 0.2];
colBlue             = [0.18, 0.28, 0.44];
colGreen            = [0.28, 0.44, 0.28];
colGreenL           = [0.38, 0.5, 0.38];
colGreenD           = [0.18, 0.30, 0.18];
colDark             = [0.08, 0.09, 0.10];
colDark2            = [0.02, 0.21, 0.22];
colYellow           = [0.50, 0.45, 0.00]
colYellow2          = [0.4, 0.35, 0.00]
colBlk              = [0.00, 0.00, 0.00]

if cmds.window('win_tkStitchheadHelper', exists=1):
	cmds.deleteUI('win_tkStitchheadHelper')

myWindow = cmds.window('win_tkStitchheadHelper', t=('xGen Helper ' + ver), s=1, wh=(windowStartHeight, windowStartWidth ))
cmds.columnLayout(adj=1, bgc=(colGreenD[0], colGreenD[1], colGreenD[2]))
cmds.frameLayout('flStitchHeadUtils', l='Utilities', bgc=(colGreen[0], colGreen[1], colGreen[2]), cll=1, cl=0, cc=partial(cShrinkWin, 'win_tkStitchheadHelper'))
cmds.columnLayout(adj=1, bgc=(colGreenD[0], colGreenD[1], colGreenD[2]))

cmds.rowColumnLayout(nc=3, cw=[(1, 180), (2, 180), (3, 80)])
cmds.button(l='1. Import Guides', c=cImportGuides, bgc=(colGreen[0], colGreen[1], colGreen[2]))
cmds.button(l='2. Build Gear Rig', bgc=(colGreenD[0], colGreenD[1], colGreenD[2]))
cmds.button(l='3. Add Locs', c=cAddStitchLocs, bgc=(colGreen[0], colGreen[1], colGreen[2]))
# cmds.button(l='3. Rename: GRP CTRL JOIN', c=cRenameNodes, bgc=(colGreen[0], colGreen[1], colGreen[2]))
# cmds.button(l='4. Add "GRUP" at the end', c=cFindEmptyTransforms, bgc=(colGreen[0], colGreen[1], colGreen[2]))
# cmds.button(l='5. Add Attributes', c=cAddAttributes)
cmds.setParent('..')


cmds.frameLayout('flNmSpc', l='Name Spaces', bgc=(colGreen[0], colGreen[1], colGreen[2]), cll=0, cl=0)
cmds.rowColumnLayout(nc=3, cw=[(1, 180), (2, 180), (3, 80)])
cmds.button(l='Add Hierarchy To EX', c=partial(cNmSpcCreation, 'create'), bgc=(colGreenL[0], colGreenL[1], colGreenL[2]))
cmds.button(l='Remove Hierarchy From EX', c=partial(cNmSpcCreation, 'remove'), bgc=(colGreenD[0], colGreenD[1], colGreenD[2]))
cmds.button(l='Delete EX', c=partial(cNmSpcCreation, 'delete'), bgc=(colRed[0], colRed[1], colRed[2]))
cmds.setParent('..')

cmds.frameLayout('flAutoNmConv', l='Auto Naming Convention', bgc=(colGreen[0], colGreen[1], colGreen[2]), cll=0, cl=0)
cmds.rowColumnLayout(nc=2, cw=[(1, 220), (2, 220)])
cmds.button(l='Match Naming Convention Hierarchy', c=partial(cNamingConvention, 'hierarchy'), bgc=(colGreen[0], colGreen[1], colGreen[2]))
cmds.button(l='Match Naming Convention Selected', c=partial(cNamingConvention, 'selected'), bgc=(colYellow[0], colYellow[1], colYellow[2]))

cmds.setParent('..')
cmds.frameLayout('flNmConv', l='Naming Convention', bgc=(colGreen[0], colGreen[1], colGreen[2]), cll=0, cl=0)
cmds.rowColumnLayout(nc=4, cw=[(1, 110), (2, 110), (3, 110), (4, 110)])
cmds.button(l='Last --> Front', c=partial(cReorganize, 'Last --> Front'), bgc=(colYellow[0], colYellow[1], colYellow[2]))
cmds.button(l='remove Last _', c=partial(cReorganize, 'xx_yy --> xxyy'), bgc=(colRed[0], colRed[1], colRed[2]))
cmds.button(l='Switch Last', c=partial(cReorganize, 'Switch Last'), bgc=(colBlue[0], colBlue[1], colBlue[2]))
cmds.button(l='Delete Last', c=partial(cReorganize, 'Delete Last'), bgc=(colRed[0], colRed[1], colRed[2]))
cmds.button(l='_GRUP', c=partial(cReorganize, '_GRUP'), bgc=(colYellow2[0], colYellow2[1], colYellow2[2]))
cmds.button(l='_CTRL', c=partial(cReorganize, '_CTRL'), bgc=(colYellow2[0], colYellow2[1], colYellow2[2]))
cmds.button(l='_JOIN', c=partial(cReorganize, '_JOIN'), bgc=(colYellow2[0], colYellow2[1], colYellow2[2]))
cmds.button(l='_OFF_GRP', c=partial(cReorganize, '_OFF_GRP'), bgc=(colYellow2[0], colYellow2[1], colYellow2[2]))
cmds.button(l='C1 --> C_1', c=partial(cReorganize, 'C1 --> C_1'), bgc=(colYellow2[0], colYellow2[1], colYellow2[2]))
cmds.button(l='1 --> 001', c=partial(cReorganize, '1 --> 001'), bgc=(colYellow2[0], colYellow2[1], colYellow2[2]))
cmds.showWindow(myWindow)

cmds.window(myWindow, w=440, h=150, e=1)
