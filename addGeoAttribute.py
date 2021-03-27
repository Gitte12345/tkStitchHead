# tkAddStitchLocs.py
# mar 2021
# Thomas Kutschera
# add locators

import maya.cmds as cmds
import maya.mel as mel

carry = cmds.ls(sl=1, l=1)[0]
geoGrp = cmds.ls(sl=1, l=1)[1]
cmds.addAttr(carry, ln='geo', at='enum', en='normal:template:reference')
cmds.setAttr(carry + '.geo', e=1, keyable=1)
cmds.setAttr(geoGrp + '.overrideEnabled', 1)
cmds.setAttr (geoGrp + '.overrideEnabled', 1)
cmds.connectAttr(carry + '.geo', geoGrp + '.overrideDisplayType')


# addAttr -ln "geo"  -at "enum" -en "normal:template:reference:"  |rig|world_C1_ctl;
# setAttr -e-keyable true |rig|world_C1_ctl.geo;