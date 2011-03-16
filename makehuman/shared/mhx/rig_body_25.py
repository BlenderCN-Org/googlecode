""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
Body bone definitions 

"""

import mhx_rig, mhx_spine
from mhx_rig import *
from mhx_spine import spineDeform

BodyJoints = [
	('root-tail',			'o', ('spine3', [0,-1,0])),
	('hips-tail',			'o', ('pelvis', [0,-1,0])),
	('mid-uplegs',			'l', ((0.5, 'l-upper-leg'), (0.5, 'r-upper-leg'))),
	#('spine0',				'l', ((0.5, 'spine1'), (0.5, 'neck'))),

	('r-breast1',			'v', 3559),
	('r-breast2',			'v', 2944),
	('r-breast',			'l', ((0.4, 'r-breast1'), (0.6, 'r-breast2'))),
	('r-tit',				'v', 3718),

	('l-breast1',			'v', 10233),
	('l-breast2',			'v', 10776),
	('l-breast',			'l', ((0.4, 'l-breast1'), (0.6, 'l-breast2'))),
	('l-tit',				'v', 10115),

	('mid-rib-top',			'v', 7273),
	('mid-rib-bot',			'v', 6905),

	('abdomen-front',		'v', 7359),
	('abdomen-back',		'v', 7186),
	('stomach-top',			'v', 7336),
	('stomach-bot',			'v', 7297),
	('stomach-front',		'v', 7313),
	('stomach-back',		'v', 7472),

	('penis-tip',			'v', 7415),
	('r-penis',				'v', 2792),
	('l-penis',				'v', 7448),
	('penis-root',			'l', ((0.5, 'r-penis'), (0.5, 'l-penis'))),
	('scrotum-tip',			'v', 7444),
	('r-scrotum',			'v', 2807),
	('l-scrotum',			'v', 7425),
	('scrotum-root',		'l', ((0.5, 'r-scrotum'), (0.5, 'l-scrotum'))),

	('r-toe-1-1',			'j', 'r-toe-1-1'),
	('l-toe-1-1',			'j', 'l-toe-1-1'),
	('mid-feet',			'l', ((0.5, 'l-toe-1-1'), (0.5, 'r-toe-1-1'))),
	('floor',				'o', ('mid-feet', [0,-0.3,0])),
]

BodyHeadsTails = [
	('MasterFloor',			'floor', ('floor', zunit)),
	('MasterHips',			'pelvis', ('pelvis', zunit)),
	('MasterNeck',			'neck', ('neck', zunit)),

	('Root',				'root-tail', 'spine3'),
	('BendRoot',			'spine3', ('spine3', yunit)),
	('Hips',				'spine3', 'root-tail'),
	('Pelvis',				'pelvis', 'spine3'),
	('Spine1',				'spine3', 'spine2'),
	('Spine2',				'spine2', 'spine1'),
	('Spine3',				'spine1', 'neck'),
	('Spine4',				'neck', ('neck', [0,0.5,0])),

	('DfmHips',				'spine3', 'root-tail'),
	('DfmSpine1',			'spine3', 'spine2'),
	('DfmSpine2',			'spine2', 'spine1'),
	('DfmSpine3',			'spine1', 'neck'),

	('Shoulders',			'neck', ('neck', [0,0.5,0])),
	('SpineBender',			'spine3', 'neck'),

	('LowerNeck',			('neck', [0,-0.5,0]), 'neck'),
	('Neck',				'neck', 'head'),
	('Head',				'head', 'head-end'),
	('DfmNeck',				'neck', 'head'),
	('DfmHead',				'head', 'head-end'),

	('DfmRib',				'mid-rib-top', 'mid-rib-bot'),
	('RibTarget',			'spine2', 'mid-rib-bot'),
	('DfmStomach',			'mid-rib-bot', 'stomach-bot'),
	('HipBone',				'root-tail', 'stomach-bot'),
	('Breathe',				'mid-rib-bot', ('mid-rib-bot', zunit)),
	('Breast_L',			'r-breast', 'r-tit'),
	('Breast_R',			'l-breast', 'l-tit'),

	('Penis',				'penis-root', 'penis-tip'),
	('Scrotum',				'scrotum-root', 'scrotum-tip'),
]

BodyArmature = [
	('MasterFloor',		0.0, None, F_WIR, L_MAIN, NoBB),
	('MasterHips',		0.0, None, F_WIR+F_HID, L_MAIN, NoBB),
	('MasterNeck',		0.0, None, F_WIR+F_HID, L_MAIN, NoBB),

	('Root',			0.0, Master, F_WIR, L_MAIN+L_SPINEFK+L_SPINEIK, NoBB),
	('BendRoot',		0.0, 'Root', 0, L_HELP, NoBB),
	('Hips',			0.0, 'Root', F_WIR, L_SPINEFK+L_SPINEIK, NoBB),

	('Spine1',			0.0, 'Root', F_WIR, L_SPINEFK, NoBB),
	('Spine2',			0.0, 'Spine1', F_WIR, L_SPINEFK, NoBB),
	('Spine3',			0.0, 'Spine2', F_WIR, L_SPINEFK, NoBB),

	('Shoulders',		0.0, 'Root', F_WIR, L_SPINEIK, NoBB),
	('SpineBender',		0.0, 'Root', 0, L_HELP, NoBB),

	('Neck',			0.0, 'Spine3', F_WIR, L_SPINEIK+L_SPINEFK+L_HEAD, NoBB),
	('Head',			0.0, 'Neck', F_WIR, L_SPINEIK+L_SPINEFK+L_HEAD, NoBB),

	('DfmHips',			0.0, 'Root', F_DEF, L_DMAIN, NoBB),
	('DfmSpine1',		0.0, 'Root', F_DEF+F_CON, L_DMAIN, (1,1,3) ),
	('DfmSpine2',		0.0, 'Spine1', F_DEF+F_CON, L_DMAIN, (1,1,3) ),
	('DfmSpine3',		0.0, 'Spine2', F_DEF+F_CON, L_DMAIN, (1,1,3) ),
	('DfmNeck',			0.0, 'Spine3', F_DEF+F_CON, L_DMAIN, (1,1,3) ),
	('DfmHead',			0.0, 'Neck', F_DEF+F_CON, L_DMAIN, NoBB),

	('DfmRib',			0.0, 'Spine3', F_DEF, L_DMAIN, NoBB),
	('RibTarget',		0.0, 'Spine2', 0, L_TORSO, NoBB),
	('DfmStomach',		0.0, 'DfmRib', F_DEF+F_CON, L_DMAIN, NoBB),
	('HipBone',			0.0, 'Hips', 0, L_HELP, NoBB),

	('Breast_L',		-45*D, 'DfmRib', F_DEF, L_DEF, NoBB),
	('Breast_R',		45*D, 'DfmRib', F_DEF, L_DEF, NoBB),
	('Breathe',			0.0, 'DfmRib', F_WIR, L_TORSO, NoBB),

	('Penis',			0.0, 'Hips', 0, L_TORSO, (1,5,1) ),
	('Scrotum',			0.0, 'Hips', 0, L_TORSO, NoBB),

	('Penis',			0.0, 'Hips', F_DEF, L_DEF, (1,5,1) ),
	('Scrotum',			0.0, 'Hips', F_DEF, L_DEF, NoBB),
]

#
#	BodyControlPoses(fp):
#

limBreastRot = (-45*D,45*D, -10*D,10*D, -20*D,20*D)
limBreastScale =  (0.8,1.25, 0.7,1.5, 0.8,1.25)

def BodyControlPoses(fp):
	addPoseBone(fp,  'MasterFloor', 'GZM_Root', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp,  'MasterHips', 'GZM_Root', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_HID, [])

	addPoseBone(fp,  'MasterNeck', 'GZM_Root', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_HID, [])

	addPoseBone(fp,  'Root', 'MHHips', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, mhx_rig.rootChildOfConstraints)

	addPoseBone(fp,  'Hips', 'GZM_CircleHips', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-50*D,40*D, -45*D,45*D, -16*D,16*D), (1,1,1)])])

	#addPoseBone(fp,  'Hip_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	#addPoseBone(fp,  'Hip_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	# Spine FK
	addPoseBone(fp,  'Spine1', 'GZM_CircleSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH, 
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-60*D,90*D, -60*D,60*D, -60*D,60*D), (1,1,1)]),
		 ('CopyRot', C_LOCAL, 0, ['Rot', 'SpineBender', (1,1,1), (0,0,0), False]),
		])

	addPoseBone(fp,  'Spine2', 'GZM_CircleSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-90*D,70*D, -20*D,20*D, -50*D,50*D), (1,1,1)]),
		 ('CopyRot', C_LOCAL, 0, ['Rot', 'SpineBender', (1,1,1), (0,0,0), False]),
		])

	addPoseBone(fp,  'Spine3', 'GZM_CircleChest', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-20*D,20*D, 0,0, -20*D,20*D), (1,1,1)]),
		 ('CopyRot', C_LOCAL, 0, ['Rot', 'SpineBender', (1,1,1), (0,0,0), False]),
	])

	# Spine IK
	addPoseBone(fp,  'Shoulders', 'GZM_IK_Shoulder', 'Spine', (0,0,0), (1,0,1), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (0,0, -45*D,45*D, 0,0), (1,1,1)]),
		 ('LimitDist', 0, 1, ['LimitDist', 'Root', 'INSIDE'])])

	addPoseBone(fp,  'SpineBender', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
		 [('IK', 0, 1, ['SpineIK', 'Shoulders', 1, None, (True, False,True)]),
		 ('CopyRot', C_LOCAL, 1, ['Rot', 'Shoulders', (0,1,0), (0,0,0), True]),
	])

	# Neck and head
	addPoseBone(fp,  'Neck', 'MHNeck', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-60*D,40*D, -45*D,45*D, -60*D,60*D), (1,1,1)])])

	addPoseBone(fp,  'Head', 'MHHead', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-60*D,40*D, -60*D,60*D, -45*D,45*D), (1,1,1)])])

	# Torso
	addPoseBone(fp,  'DfmRib', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('StretchTo', 0, 1, ['Stretch', 'RibTarget', 1])])

	addPoseBone(fp,  'DfmStomach',None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('StretchTo', C_STRVOL, 1, ['Stretch', 'HipBone', 1]),
		])

	addPoseBone(fp, 'RibTarget', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'HipBone', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp,  'Breathe', 'MHCube01', None, (1,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp,  'Breast_L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, 
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limBreastRot, (1,1,1)]),
		 ('LimitScale', C_OW_LOCAL, 1, ['Scale', limBreastScale, (1,1,1)])	])

	addPoseBone(fp,  'Breast_R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limBreastRot, (1,1,1)]),
		 ('LimitScale', C_OW_LOCAL, 1, ['Scale', limBreastScale, (1,1,1)])	])

	addPoseBone(fp,  'Penis', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

	addPoseBone(fp,  'Scrotum', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

	copyDeform(fp, 'DfmHips', 'Hips', 0, U_LOC+U_ROT, None, [])
	copyDeform(fp, 'DfmSpine1', 'Spine1', 0, U_LOC+U_ROT, None, [])
	copyDeform(fp, 'DfmSpine2', 'Spine2', 0, U_ROT, None, [])
	copyDeform(fp, 'DfmSpine3', 'Spine3', 0, U_ROT, None, [])
	copyDeform(fp, 'DfmNeck', 'Neck', 0, U_ROT, None, [])
	copyDeform(fp, 'DfmHead', 'Head', 0, U_ROT, None, [])
	return

#
#	BodyShapeDrivers
#	Shape : (driver, channel, coeff)
#

BodyShapeDrivers = {
	'BreatheIn' : ('Breathe', 'LOC_Z', ('0', '2.0')), 
}

#
#	BodyShapeKeyScale = {
#

BodyShapeKeyScale = {
	'BreatheIn'			: ('spine1', 'neck', 1.89623),
	'BicepFlex'			: ('r-uparm-front', 'r-uparm-back', 0.93219),
}

BodySpines = [
	('Spine', ['Spine1IK', 'Spine2IK', 'Spine3IK', 'Spine4IK', 'Shoulders'])
]



