import maya.cmds as cmds

exception = ['geo_C_001_GRUP', 'rig_C_001_GRUP', 'JOIN_org']
suffix = [
'Ctl', '_CTRL', 'Crv', '_NCRV', 'Parentconstraint1', '_DPAR', 'Scaleconstraint1', '_DSCC', 'Pointconstraint1', '_DPOC', 'Orientconstraint1', '_DORC'
]

cmds.select('rig', r=1)
entry_trs = cmds.ls(sl=1)[0]
childs = cmds.listRelatives(entry_trs, ad=1)
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
	if shps:
		pass
	if cmds.objectType(node, isType='ikEffector') or cmds.objectType(node, isType='joint'):
		pass
	else:
		if node not in exception:
			newName += '_GRUP'


 	print newName
 	print str(node) + ' --> ' + str(newName)
 	new = str(newName)
 	if len(new) != 0:
		cmds.rename(node, newName)

