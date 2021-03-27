# tkGetCenter.py
# place a locator in the middle of the selection

import maya.cmds as cmds
import maya.mel as mel

def tkGetCenter(*args):
    posX = 0.0
    posY = 0.0
    posZ = 0.0

    mySel = cmds.ls(sl=1,l=1)
    mel.eval('ConvertSelectionToVertices')
    vertices = cmds.ls(sl=1, l=1)
    vertices = cmds.filterExpand(ex=1, sm=31)

    amount = len(vertices)

    for v in vertices:
        pos = cmds.xform(v, q=1, translation=1, ws=1)
        posX += pos[0]
        posY += pos[1]
        posZ += pos[2]

    centerPos = (posX/amount, posY/amount, posZ/amount) 
    LC = cmds.spaceLocator(p=centerPos)
    lc = cmds.listRelatives(LC, s=1)
    cmds.setAttr(lc + '.localScaleX', .1)
    cmds.setAttr(lc + '.localScaleY', .1)
    cmds.setAttr(lc + '.localScaleZ', .1)
    cmds.select(mySel, r=1)
    return centerPos
    
tkGetCenter()