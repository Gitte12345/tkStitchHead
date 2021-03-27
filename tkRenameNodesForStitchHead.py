# rename nodes to match stitchhead guideline

import maya.cmds as cmds

grpsA   = cmds.ls('*grp')
print 'grp:'
if grpsA:
    for grp in grpsA:
        short = grp.split('|')[-1] 
        new = short.replace('grp','GRUP')
        cmds.rename(grp, new)
        print (grp + ' --> ' + new)
    

grpsB   = cmds.ls('*GRP', l=1)
print 'GRP:'
if grpsB:
    for grp in grpsB:
        short = grp.split('|')[-1] 
        new = short.replace('GRP','GRUP')
        cmds.rename(grp, new)
        print (grp + ' --> ' + new)
    
cons    = cmds.ls('*ctl', l=1)
print 'ctl:'
if cons:
    for con in cons:
        short = con.split('|')[-1] 
        new = short.replace('ctl','CTRL')
        cmds.rename(con, new)  
        print (con + ' --> ' + new)
        
pars    = cmds.ls('*parentConstraint1', l=1)
print 'parentConstraints:'
if pars:
    for par in pars:
        short = par.split('|')[-1] 
        new = short.replace('parentConstraint1','DPAR')
        cmds.rename(par, new)  
        print (par + ' --> ' + new)
    
roots   = cmds.ls('*root', l=1)
print 'roots:'
if roots:
    for root in roots:
        short = root.split('|')[-1] 
        new = short.replace('root','ROOT')
        cmds.rename(root, new)
        print (root + ' --> ' + new)
    
numCs   = cmds.ls('*_C1*', l=1)
print 'C1:'
if numCs:
    for numC in numCs:
        short = short.split('|')[-1] 
        new = short.replace('_C1','_C_001')
        cmds.rename(numC, new)
        print (numC + ' --> ' + new)