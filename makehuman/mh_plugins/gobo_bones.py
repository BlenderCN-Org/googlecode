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
Bones for the Gobo rig

"""

import mhxbones

joints = [
	('mid-feet'			,'l', ((0.5, 'l-ankle'), (0.5, 'r-ankle'))),
	('root_head'			, 'o', ('mid-feet', [0,-0.3,0])),
	('root_tail'			, 'o', ('root_head', [0,0,-1])),
	('hand_L_head'			, 'j', 'r-hand'),
	('hand_L_tail'			, 'j', 'r-finger-3-3'),
	('hand_R_head'			, 'j', 'l-hand'),
	('hand_R_tail'			, 'j', 'l-finger-3-3'),
	('hip_head'			, 'j', 'spine3'),
	('hip_tail'			, 'j', 'pelvis'),
	('spine_3_head'			, 'j', 'spine3'),
	('spine_3_tail'			, 'j', 'spine2'),
	('spine_2_tail'			, 'j', 'spine1'),
	('spine_1_tail'			, 'j', 'neck'),
	('neck_tail'			, 'j', 'head'),
	('head_tail'			, 'l', ((2.0, 'head'), (-1.0, 'neck'))),
	('jaw_head'			, 'j', 'mouth'),
	('jaw_tail'			, 'v', 8162),

	('eye_L'			, 'j', 'r-eye'),
	('eye_R'			, 'j', 'l-eye'),
	('mid-eyes'			, 'l', ((0.5, 'l-eye'), (0.5, 'r-eye'))), 
	('r-eye-front'			, 'o', ('r-eye', [0,0,0.3])),
	('l-eye-front'			, 'o', ('l-eye', [0,0,0.3])),

	('gaze_head'			, 'o', ('mid-eyes', [0,0,5.25])),
	('gaze_tail'			, 'o', ('gaze_head', [0,0,-1])),
	('gaze_L_head'			, 'o', ('r-eye', [0,0,5.25])),
	('gaze_L_tail'			, 'o', ('gaze_L_head', [0,0,-1])),
	('gaze_R_head'			, 'o', ('l-eye', [0,0,5.25])),
	('gaze_R_tail'			, 'o', ('gaze_R_head', [0,0,-1])),

	('chest-front'			,'v', 7292 ),
	('jaw-tip'			,'v', 8162 ),
	('tounge-tip'			,'v', 8049 ),
	('tounge-mid'			,'v', 8103 ),
	('tounge-root'			,'v', 8099 ),
	('l-uplid'			,'v', 12630 ),
	('l-lolid'			,'v', 12594 ),
	('r-uplid'			,'v', 2442 ),
	('r-lolid'			,'v', 2520 ),

	('shoulder_L_head'		, 'j', 'r-clavicle'),
	('shoulder_L_tail'		, 'j', 'r-shoulder'),
	('ikfk_hand_L_head'		, 'o', ('r-finger-3-3', [2,0,0])),
	('ikfk_hand_L_tail'		, 'o', ('ikfk_hand_L_head', [-1,0,0])),
	('arm_root_L_head'		, 'j', 'r-clavicle'),
	('arm_root_L_tail'		, 'j', 'r-shoulder'),
	('armupper_L_tail'		, 'j', 'r-elbow'),
	('armlower_L_tail'		, 'j', 'r-hand'),
	('hand_L_head'			, 'j', 'r-hand'),
	('hand_L_tail'			, 'j', 'r-finger-3-1'),
	('finger_curl_L_head'		, 'o', ('r-hand', [0, 1.0, 0])),
	('finger_curl_L_tail'		, 'o', ('finger_curl_L_head', [0, 1.0, 0])),
	('elbow_L_head'			, 'o', ('arm_root_L_tail', [0,0,-1])),
	('elbow_L_tail'			, 'o', ('elbow_L_head', [0,0.3,0])),

	('shoulder_R_head'		, 'j', 'l-clavicle'),
	('shoulder_R_tail'		, 'j', 'l-shoulder'),
	('ikfk_hand_R_head'		, 'o', ('l-finger-3-3', [-2,0,0])),
	('ikfk_hand_R_tail'		, 'o', ('ikfk_hand_R_head', [1,0,0])),
	('arm_root_R_head'		, 'j', 'l-clavicle'),
	('arm_root_R_tail'		, 'j', 'l-shoulder'),
	('armupper_R_tail'		, 'j', 'l-elbow'),
	('armlower_R_tail'		, 'j', 'l-hand'),
	('hand_R_head'			, 'j', 'l-hand'),
	('hand_R_tail'			, 'j', 'l-finger-3-1'),
	('finger_curl_R_head'		, 'o', ('l-hand', [0, 1.0, 0])),
	('finger_curl_R_tail'		, 'o', ('finger_curl_R_head', [0, 1.0, 0])),
	('elbow_R_head'			, 'o', ('arm_root_R_tail', [0,0,-1])),
	('elbow_R_tail'			, 'o', ('elbow_R_head', [0,0.3,0])),

	('finger-1-1_L_head'		, 'j', 'r-hand'),
	('finger-1-1_L_tail'		, 'j', 'r-finger-1-1'),
	('finger-1-2_L_tail'		, 'j', 'r-finger-1-2'),
	('finger-1-3_L_tail'		, 'l', ((2,'r-finger-1-2'), (-1,'r-finger-1-1'))),
	('finger-2-1_L_head'		, 'j', 'r-finger-2-1'),
	('finger-2-1_L_tail'		, 'j', 'r-finger-2-2'),
	('finger-2-2_L_tail'		, 'j', 'r-finger-2-3'),
	('finger-2-3_L_tail'		, 'l', ((2,'r-finger-2-3'), (-1,'r-finger-2-2'))),
	('finger-3-1_L_head'		, 'j', 'r-finger-3-1'),
	('finger-3-1_L_tail'		, 'j', 'r-finger-3-2'),
	('finger-3-2_L_tail'		, 'j', 'r-finger-3-3'),
	('finger-3-3_L_tail'		, 'l', ((2,'r-finger-3-3'), (-1,'r-finger-3-2'))),
	('finger-4-1_L_head'		, 'j', 'r-finger-4-1'),
	('finger-4-1_L_tail'		, 'j', 'r-finger-4-2'),
	('finger-4-2_L_tail'		, 'j', 'r-finger-4-3'),
	('finger-4-3_L_tail'		, 'l', ((2,'r-finger-4-3'), (-1,'r-finger-4-2'))),
	('finger-5-1_L_head'		, 'j', 'r-finger-5-1'),
	('finger-5-1_L_tail'		, 'j', 'r-finger-5-2'),
	('finger-5-2_L_tail'		, 'j', 'r-finger-5-3'),
	('finger-5-3_L_tail'		, 'l', ((2,'r-finger-5-3'), (-1,'r-finger-5-2'))),

	('finger-1-1_R_head'		, 'j', 'l-hand'),
	('finger-1-1_R_tail'		, 'j', 'l-finger-1-1'),
	('finger-1-2_R_tail'		, 'j', 'l-finger-1-2'),
	('finger-1-3_R_tail'		, 'l', ((2,'l-finger-1-2'), (-1,'l-finger-1-1'))),
	('finger-2-1_R_head'		, 'j', 'l-finger-2-1'),
	('finger-2-1_R_tail'		, 'j', 'l-finger-2-2'),
	('finger-2-2_R_tail'		, 'j', 'l-finger-2-3'),
	('finger-2-3_R_tail'		, 'l', ((2,'l-finger-2-3'), (-1,'l-finger-2-2'))),
	('finger-3-1_R_head'		, 'j', 'l-finger-3-1'),
	('finger-3-1_R_tail'		, 'j', 'l-finger-3-2'),
	('finger-3-2_R_tail'		, 'j', 'l-finger-3-3'),
	('finger-3-3_R_tail'		, 'l', ((2,'l-finger-3-3'), (-1,'l-finger-3-2'))),
	('finger-4-1_R_head'		, 'j', 'l-finger-4-1'),
	('finger-4-1_R_tail'		, 'j', 'l-finger-4-2'),
	('finger-4-2_R_tail'		, 'j', 'l-finger-4-3'),
	('finger-4-3_R_tail'		, 'l', ((2,'l-finger-4-3'), (-1,'l-finger-4-2'))),
	('finger-5-1_R_head'		, 'j', 'l-finger-5-1'),
	('finger-5-1_R_tail'		, 'j', 'l-finger-5-2'),
	('finger-5-2_R_tail'		, 'j', 'l-finger-5-3'),
	('finger-5-3_R_tail'		, 'l', ((2,'l-finger-5-3'), (-1,'l-finger-5-2'))),

	('toe-1-1_L_head'		, 'j', 'r-toe-1-1'),
	('toe-1-1_L_tail'		, 'j', 'r-toe-1-2'),
	('toe-1-2_L_tail'		, 'l', ((2,'toe-1-1_L_tail'), (-1,'toe-1-1_L_head'))),
	('toe-2-1_L_head'		, 'j', 'r-toe-2-1'),
	('toe-2-1_L_tail'		, 'j', 'r-toe-2-2'),
	('toe-2-2_L_tail'		, 'j', 'r-toe-2-3'),
	('toe-2-3_L_tail'		, 'l', ((2,'toe-2-2_L_tail'), (-1,'toe-2-1_L_tail'))),
	('toe-3-1_L_head'		, 'j', 'r-toe-3-1'),
	('toe-3-1_L_tail'		, 'j', 'r-toe-3-2'),
	('toe-3-2_L_tail'		, 'j', 'r-toe-3-3'),
	('toe-3-3_L_tail'		, 'l', ((2,'toe-3-2_L_tail'), (-1,'toe-3-1_L_tail'))),
	('toe-4-1_L_head'		, 'j', 'r-toe-4-1'),
	('toe-4-1_L_tail'		, 'j', 'r-toe-4-2'),
	('toe-4-2_L_tail'		, 'j', 'r-toe-4-3'),
	('toe-4-3_L_tail'		, 'l', ((2,'toe-4-2_L_tail'), (-1,'toe-4-1_L_tail'))),
	('toe-5-1_L_head'		, 'j', 'r-toe-5-1'),
	('toe-5-1_L_tail'		, 'j', 'r-toe-5-2'),
	('toe-5-2_L_tail'		, 'j', 'r-toe-5-3'),
	('toe-5-3_L_tail'		, 'l', ((2,'toe-5-2_L_tail'), (-1,'toe-5-1_L_tail'))),

	('toe-1-1_R_head'		, 'j', 'l-toe-1-1'),
	('toe-1-1_R_tail'		, 'j', 'l-toe-1-2'),
	('toe-1-2_R_tail'		, 'l', ((2,'toe-1-1_R_tail'), (-1,'toe-1-1_R_head'))),
	('toe-2-1_R_head'		, 'j', 'l-toe-2-1'),
	('toe-2-1_R_tail'		, 'j', 'l-toe-2-2'),
	('toe-2-2_R_tail'		, 'j', 'l-toe-2-3'),
	('toe-2-3_R_tail'		, 'l', ((2,'toe-2-2_R_tail'), (-1,'toe-2-1_R_tail'))),
	('toe-3-1_R_head'		, 'j', 'l-toe-3-1'),
	('toe-3-1_R_tail'		, 'j', 'l-toe-3-2'),
	('toe-3-2_R_tail'		, 'j', 'l-toe-3-3'),
	('toe-3-3_R_tail'		, 'l', ((2,'toe-3-2_R_tail'), (-1,'toe-3-1_R_tail'))),
	('toe-4-1_R_head'		, 'j', 'l-toe-4-1'),
	('toe-4-1_R_tail'		, 'j', 'l-toe-4-2'),
	('toe-4-2_R_tail'		, 'j', 'l-toe-4-3'),
	('toe-4-3_R_tail'		, 'l', ((2,'toe-4-2_R_tail'), (-1,'toe-4-1_R_tail'))),
	('toe-5-1_R_head'		, 'j', 'l-toe-5-1'),
	('toe-5-1_R_tail'		, 'j', 'l-toe-5-2'),
	('toe-5-2_R_tail'		, 'j', 'l-toe-5-3'),
	('toe-5-3_R_tail'		, 'l', ((2,'toe-5-2_R_tail'), (-1,'toe-5-1_R_tail'))),

	('thigh_root_L_head'		, 'l', ((0.5, 'pelvis'), (0.5, 'r-upper-leg'))),
	('thigh_root_L_tail'		, 'j', 'r-upper-leg'),
	('thigh_L_tail'			, 'j', 'r-knee'),
	('shin_L_tail'			, 'j', 'r-ankle'),
	('foot_L_tail'			, 'b', 'toe-3-1_L_head'),
	('toe_L_tail'			, 'v', 12258),

	('thigh_root_R_head'		, 'l', ((0.5, 'pelvis'), (0.5, 'l-upper-leg'))),
	('thigh_root_R_tail'		, 'j', 'l-upper-leg'),
	('thigh_R_tail'			, 'j', 'l-knee'),
	('shin_R_tail'			, 'j', 'l-ankle'),
	('foot_R_tail'			, 'b', 'toe-3-1_R_head'),
	('toe_R_tail'			, 'v', 13258),

	('footCtrl_L_head'		, 'o', ('shin_L_tail', [0,-0.3,-0.3])),
	('footCtrl_L_tail'		, 'o', ('footCtrl_L_head', [0,1.5,0])),
	('tiptoe_L_head'		, 'b', 'toe_L_tail'),
	('tiptoe_L_tail'		, 'o', ('tiptoe_L_head', [0,0,0.3])),
	('tumble_out_L_head'		, 'v', 4000),
	('tumble_out_L_tail'		, 'o', ('tumble_out_L_head', [0,0.3,0])),
	('tumble_in_L_head'		, 'v', 4003),
	('tumble_in_L_tail'		, 'o', ('tumble_in_L_head', [0,0.3,0])),
	('heel_L_head'			, 'v', 5721),
	('heel_L_tail'			, 'o', ('heel_L_head', [0,0.3,0])),
	('rotate_toe_L_head'		, 'b', 'foot_L_tail'),
	('rotate_toe_L_tail'		, 'o', ('rotate_toe_L_head', [0,0.3,0])),
	('toe_target_L_head'		, 'b', 'toe_L_tail'),
	('toe_target_L_tail'		, 'l', ((2, 'toe_L_tail'), (-1, 'foot_L_tail'))),
	('foot_target_L_head'		, 'b', 'foot_L_tail'),
	('foot_target_L_tail'		, 'l', ((2, 'foot_L_tail'), (-1, 'shin_L_tail'))),
	('leg_target_L_head'		, 'b', 'shin_L_tail'),
	('leg_target_L_tail'		, 'l', ((2, 'shin_L_tail'), (-1, 'thigh_L_tail'))),
	('foot_tumble_L_head'		, 'o', ('tiptoe_L_head', [0,0,1.0])),
	('foot_tumble_L_tail'		, 'o', ('foot_tumble_L_head', [0,0.3,0])),
	('foot_Roll_L_head'		, 'o', ('toe_L_tail', [-0.15,0,0.3])),
	('foot_Roll_L_tail'		, 'o', ('toe_L_tail', [0.15,0,0.3])),
	('knee_L_head'			, 'o', ('thigh_L_tail', [0,0,4.0])),
	('knee_L_tail'			, 'o', ('knee_L_head', [0,0.3,0])),
	('ikfk_foot_L_head'		, 'o', ('foot_L_tail', [0,0,1.0])),
	('ikfk_foot_L_tail'		, 'o', ('ikfk_foot_L_head', [0,0.3,0])),

	('footCtrl_R_head'		, 'o', ('shin_R_tail', [0,-0.3,-0.3])),
	('footCtrl_R_tail'		, 'o', ('footCtrl_R_head', [0,1.5,0])),
	('tiptoe_R_head'		, 'b', 'toe_R_tail'),
	('tiptoe_R_tail'		, 'o', ('tiptoe_R_head', [0,0,0.3])),
	('tumble_out_R_head'		, 'v', 14003),
	('tumble_out_R_tail'		, 'o', ('tumble_out_R_head', [0,0.3,0])),
	('tumble_in_R_head'		, 'v', 13998),
	('tumble_in_R_tail'		, 'o', ('tumble_in_R_head', [0,0.3,0])),
	('heel_R_head'			, 'v', 13338),
	('heel_R_tail'			, 'o', ('heel_R_head', [0,0.3,0])),
	('rotate_toe_R_head'		, 'b', 'foot_R_tail'),
	('rotate_toe_R_tail'		, 'o', ('rotate_toe_R_head', [0,0.3,0])),
	('toe_target_R_head'		, 'b', 'toe_R_tail'),
	('toe_target_R_tail'		, 'l', ((2, 'toe_R_tail'), (-1, 'foot_R_tail'))),
	('foot_target_R_head'		, 'b', 'foot_R_tail'),
	('foot_target_R_tail'		, 'l', ((2, 'foot_R_tail'), (-1, 'shin_R_tail'))),
	('leg_target_R_head'		, 'b', 'shin_R_tail'),
	('leg_target_R_tail'		, 'l', ((2, 'shin_R_tail'), (-1, 'thigh_R_tail'))),
	('foot_tumble_R_head'		, 'o', ('tiptoe_R_head', [0,0,1.0])),
	('foot_tumble_R_tail'		, 'o', ('foot_tumble_R_head', [0,0.3,0])),
	('foot_Roll_R_head'		, 'o', ('toe_R_tail', [-0.15,0,1.5])),
	('foot_Roll_R_tail'		, 'o', ('foot_Roll_R_head', [0.3,0,0])),
	('knee_R_head'			, 'o', ('thigh_R_tail', [0,0,4.0])),
	('knee_R_tail'			, 'o', ('knee_R_head', [0,0.3,0])),
	('ikfk_foot_R_head'		, 'o', ('foot_R_tail', [0,0,1.0])),
	('ikfk_foot_R_tail'		, 'o', ('ikfk_foot_R_head', [0,0.3,0])),
]

headsTails = [
	('Root'			, 'root_head', 'root_tail'),
	('HandCtrl_L'		, 'hand_L_head', 'hand_L_tail'),
	('HandCtrl_R'		, 'hand_R_head', 'hand_R_tail'),
	('Hips'			, 'hip_head', 'hip_tail'),
	('Spine3'		, 'spine_3_head', 'spine_3_tail'),
	('Spine2'		, 'spine_3_tail', 'spine_2_tail'),
	('Spine1'		, 'spine_2_tail', 'spine_1_tail'),
	('Neck'			, 'spine_1_tail', 'neck_tail'),
	('Head'			, 'neck_tail', 'head_tail'),
	('Jaw'			, 'jaw_head', 'jaw_tail'),

	('Clavicle_L'		, 'shoulder_L_head', 'shoulder_L_tail'),
	('ikfkHand_L'		, 'ikfk_hand_L_head', 'ikfk_hand_L_tail'),
	('ArmRoot_L'		, 'arm_root_L_head', 'arm_root_L_tail'),
	('UpArm_L'		, 'arm_root_L_tail', 'armupper_L_tail'),
	('LoArm_L'		, 'armupper_L_tail', 'armlower_L_tail'),
	('Hand_L'		, 'armlower_L_tail', 'hand_L_tail'),

	('UpArm_ik_L'		, 'arm_root_L_tail', 'armupper_L_tail'),
	('LoArm_ik_L'		, 'armupper_L_tail', 'armlower_L_tail'),
	('Hand_ik_L'		, 'armlower_L_tail', 'hand_L_tail'),
	('FingerCurl_ik_L'	, 'finger_curl_L_head', 'finger_curl_L_tail'),
	('UpArm_fk_L'		, 'arm_root_L_tail', 'armupper_L_tail'),
	('LoArm_fk_L'		, 'armupper_L_tail', 'armlower_L_tail'),
	('FingerCurl_fk_L'	, 'finger_curl_L_head', 'finger_curl_L_tail'),
	('Hand_fk_L'		, 'hand_L_head', 'hand_L_tail'),
	('Elbow_L'		, 'elbow_L_head', 'elbow_L_tail'),

	('Finger-1-1_L'		, 'finger-1-1_L_head', 'finger-1-1_L_tail'),
	('Finger-1-2_L'		, 'finger-1-1_L_tail', 'finger-1-2_L_tail'),
	('Finger-1-3_L'		, 'finger-1-2_L_tail', 'finger-1-3_L_tail'),
	('Finger-2-1_L'		, 'finger-2-1_L_head', 'finger-2-1_L_tail'),
	('Finger-2-2_L'		, 'finger-2-1_L_tail', 'finger-2-2_L_tail'),
	('Finger-2-3_L'		, 'finger-2-2_L_tail', 'finger-2-3_L_tail'),
	('Finger-3-1_L'		, 'finger-3-1_L_head', 'finger-3-1_L_tail'),
	('Finger-3-2_L'		, 'finger-3-1_L_tail', 'finger-3-2_L_tail'),
	('Finger-3-3_L'		, 'finger-3-2_L_tail', 'finger-3-3_L_tail'),
	('Finger-4-1_L'		, 'finger-4-1_L_head', 'finger-4-1_L_tail'),
	('Finger-4-2_L'		, 'finger-4-1_L_tail', 'finger-4-2_L_tail'),
	('Finger-4-3_L'		, 'finger-4-2_L_tail', 'finger-4-3_L_tail'),
	('Finger-5-1_L'		, 'finger-5-1_L_head', 'finger-5-1_L_tail'),
	('Finger-5-2_L'		, 'finger-5-1_L_tail', 'finger-5-2_L_tail'),
	('Finger-5-3_L'		, 'finger-5-2_L_tail', 'finger-5-3_L_tail'),

	('Finger-1-1_ik_L'	, 'finger-1-1_L_head', 'finger-1-1_L_tail'),
	('Finger-1-2_ik_L'	, 'finger-1-1_L_tail', 'finger-1-2_L_tail'),
	('Finger-1-3_ik_L'	, 'finger-1-2_L_tail', 'finger-1-3_L_tail'),
	('Finger-2-1_ik_L'	, 'finger-2-1_L_head', 'finger-2-1_L_tail'),
	('Finger-2-2_ik_L'	, 'finger-2-1_L_tail', 'finger-2-2_L_tail'),
	('Finger-2-3_ik_L'	, 'finger-2-2_L_tail', 'finger-2-3_L_tail'),
	('Finger-3-1_ik_L'	, 'finger-3-1_L_head', 'finger-3-1_L_tail'),
	('Finger-3-2_ik_L'	, 'finger-3-1_L_tail', 'finger-3-2_L_tail'),
	('Finger-3-3_ik_L'	, 'finger-3-2_L_tail', 'finger-3-3_L_tail'),
	('Finger-4-1_ik_L'	, 'finger-4-1_L_head', 'finger-4-1_L_tail'),
	('Finger-4-2_ik_L'	, 'finger-4-1_L_tail', 'finger-4-2_L_tail'),
	('Finger-4-3_ik_L'	, 'finger-4-2_L_tail', 'finger-4-3_L_tail'),
	('Finger-5-1_ik_L'	, 'finger-5-1_L_head', 'finger-5-1_L_tail'),
	('Finger-5-2_ik_L'	, 'finger-5-1_L_tail', 'finger-5-2_L_tail'),
	('Finger-5-3_ik_L'	, 'finger-5-2_L_tail', 'finger-5-3_L_tail'),

	('Finger-1-1_fk_L'	, 'finger-1-1_L_head', 'finger-1-1_L_tail'),
	('Finger-1-2_fk_L'	, 'finger-1-1_L_tail', 'finger-1-2_L_tail'),
	('Finger-1-3_fk_L'	, 'finger-1-2_L_tail', 'finger-1-3_L_tail'),
	('Finger-2-1_fk_L'	, 'finger-2-1_L_head', 'finger-2-1_L_tail'),
	('Finger-2-2_fk_L'	, 'finger-2-1_L_tail', 'finger-2-2_L_tail'),
	('Finger-2-3_fk_L'	, 'finger-2-2_L_tail', 'finger-2-3_L_tail'),
	('Finger-3-1_fk_L'	, 'finger-3-1_L_head', 'finger-3-1_L_tail'),
	('Finger-3-2_fk_L'	, 'finger-3-1_L_tail', 'finger-3-2_L_tail'),
	('Finger-3-3_fk_L'	, 'finger-3-2_L_tail', 'finger-3-3_L_tail'),
	('Finger-4-1_fk_L'	, 'finger-4-1_L_head', 'finger-4-1_L_tail'),
	('Finger-4-2_fk_L'	, 'finger-4-1_L_tail', 'finger-4-2_L_tail'),
	('Finger-4-3_fk_L'	, 'finger-4-2_L_tail', 'finger-4-3_L_tail'),
	('Finger-5-1_fk_L'	, 'finger-5-1_L_head', 'finger-5-1_L_tail'),
	('Finger-5-2_fk_L'	, 'finger-5-1_L_tail', 'finger-5-2_L_tail'),
	('Finger-5-3_fk_L'	, 'finger-5-2_L_tail', 'finger-5-3_L_tail'),

	('Clavicle_R'		, 'shoulder_R_head', 'shoulder_R_tail'),
	('ikfkHand_R'		, 'ikfk_hand_R_head', 'ikfk_hand_R_tail'),
	('ArmRoot_R'		, 'arm_root_R_head', 'arm_root_R_tail'),
	('UpArm_R'		, 'arm_root_R_tail', 'armupper_R_tail'),
	('LoArm_R'		, 'armupper_R_tail', 'armlower_R_tail'),
	('Hand_R'		, 'armlower_R_tail', 'hand_R_tail'),

	('UpArm_ik_R'		, 'arm_root_R_tail', 'armupper_R_tail'),
	('LoArm_ik_R'		, 'armupper_R_tail', 'armlower_R_tail'),
	('Hand_ik_R'		, 'armlower_R_tail', 'hand_R_tail'),
	('FingerCurl_ik_R'	, 'finger_curl_R_head', 'finger_curl_R_tail'),
	('UpArm_fk_R'		, 'arm_root_R_tail', 'armupper_R_tail'),
	('LoArm_fk_R'		, 'armupper_R_tail', 'armlower_R_tail'),
	('FingerCurl_fk_R'	, 'finger_curl_R_head', 'finger_curl_R_tail'),
	('Hand_fk_R'		, 'hand_R_head', 'hand_R_tail'),
	('Elbow_R'		, 'elbow_R_head', 'elbow_R_tail'),

	('Finger-1-1_R'		, 'finger-1-1_R_head', 'finger-1-1_R_tail'),
	('Finger-1-2_R'		, 'finger-1-1_R_tail', 'finger-1-2_R_tail'),
	('Finger-1-3_R'		, 'finger-1-2_R_tail', 'finger-1-3_R_tail'),
	('Finger-2-1_R'		, 'finger-2-1_R_head', 'finger-2-1_R_tail'),
	('Finger-2-2_R'		, 'finger-2-1_R_tail', 'finger-2-2_R_tail'),
	('Finger-2-3_R'		, 'finger-2-2_R_tail', 'finger-2-3_R_tail'),
	('Finger-3-1_R'		, 'finger-3-1_R_head', 'finger-3-1_R_tail'),
	('Finger-3-2_R'		, 'finger-3-1_R_tail', 'finger-3-2_R_tail'),
	('Finger-3-3_R'		, 'finger-3-2_R_tail', 'finger-3-3_R_tail'),
	('Finger-4-1_R'		, 'finger-4-1_R_head', 'finger-4-1_R_tail'),
	('Finger-4-2_R'		, 'finger-4-1_R_tail', 'finger-4-2_R_tail'),
	('Finger-4-3_R'		, 'finger-4-2_R_tail', 'finger-4-3_R_tail'),
	('Finger-5-1_R'		, 'finger-5-1_R_head', 'finger-5-1_R_tail'),
	('Finger-5-2_R'		, 'finger-5-1_R_tail', 'finger-5-2_R_tail'),
	('Finger-5-3_R'		, 'finger-5-2_R_tail', 'finger-5-3_R_tail'),

	('Finger-1-1_ik_R'	, 'finger-1-1_R_head', 'finger-1-1_R_tail'),
	('Finger-1-2_ik_R'	, 'finger-1-1_R_tail', 'finger-1-2_R_tail'),
	('Finger-1-3_ik_R'	, 'finger-1-2_R_tail', 'finger-1-3_R_tail'),
	('Finger-2-1_ik_R'	, 'finger-2-1_R_head', 'finger-2-1_R_tail'),
	('Finger-2-2_ik_R'	, 'finger-2-1_R_tail', 'finger-2-2_R_tail'),
	('Finger-2-3_ik_R'	, 'finger-2-2_R_tail', 'finger-2-3_R_tail'),
	('Finger-3-1_ik_R'	, 'finger-3-1_R_head', 'finger-3-1_R_tail'),
	('Finger-3-2_ik_R'	, 'finger-3-1_R_tail', 'finger-3-2_R_tail'),
	('Finger-3-3_ik_R'	, 'finger-3-2_R_tail', 'finger-3-3_R_tail'),
	('Finger-4-1_ik_R'	, 'finger-4-1_R_head', 'finger-4-1_R_tail'),
	('Finger-4-2_ik_R'	, 'finger-4-1_R_tail', 'finger-4-2_R_tail'),
	('Finger-4-3_ik_R'	, 'finger-4-2_R_tail', 'finger-4-3_R_tail'),
	('Finger-5-1_ik_R'	, 'finger-5-1_R_head', 'finger-5-1_R_tail'),
	('Finger-5-2_ik_R'	, 'finger-5-1_R_tail', 'finger-5-2_R_tail'),
	('Finger-5-3_ik_R'	, 'finger-5-2_R_tail', 'finger-5-3_R_tail'),

	('Finger-1-1_fk_R'	, 'finger-1-1_R_head', 'finger-1-1_R_tail'),
	('Finger-1-2_fk_R'	, 'finger-1-1_R_tail', 'finger-1-2_R_tail'),
	('Finger-1-3_fk_R'	, 'finger-1-2_R_tail', 'finger-1-3_R_tail'),
	('Finger-2-1_fk_R'	, 'finger-2-1_R_head', 'finger-2-1_R_tail'),
	('Finger-2-2_fk_R'	, 'finger-2-1_R_tail', 'finger-2-2_R_tail'),
	('Finger-2-3_fk_R'	, 'finger-2-2_R_tail', 'finger-2-3_R_tail'),
	('Finger-3-1_fk_R'	, 'finger-3-1_R_head', 'finger-3-1_R_tail'),
	('Finger-3-2_fk_R'	, 'finger-3-1_R_tail', 'finger-3-2_R_tail'),
	('Finger-3-3_fk_R'	, 'finger-3-2_R_tail', 'finger-3-3_R_tail'),
	('Finger-4-1_fk_R'	, 'finger-4-1_R_head', 'finger-4-1_R_tail'),
	('Finger-4-2_fk_R'	, 'finger-4-1_R_tail', 'finger-4-2_R_tail'),
	('Finger-4-3_fk_R'	, 'finger-4-2_R_tail', 'finger-4-3_R_tail'),
	('Finger-5-1_fk_R'	, 'finger-5-1_R_head', 'finger-5-1_R_tail'),
	('Finger-5-2_fk_R'	, 'finger-5-1_R_tail', 'finger-5-2_R_tail'),
	('Finger-5-3_fk_R'	, 'finger-5-2_R_tail', 'finger-5-3_R_tail'),

	('Hip_L'		, 'hip_tail', 'thigh_root_L_head'),
	('LegRoot_L'		, 'thigh_root_L_head', 'thigh_root_L_tail'),
	('UpLeg_fk_L'		, 'thigh_root_L_tail', 'thigh_L_tail'),
	('LoLeg_fk_L'		, 'thigh_L_tail', 'shin_L_tail'),
	('Foot_fk_L'		, 'shin_L_tail', 'foot_L_tail'),
	('Toe_fk_L'		, 'foot_L_tail', 'toe_L_tail'),
	('UpLeg_ik_L'		, 'thigh_root_L_tail', 'thigh_L_tail'),
	('LoLeg_ik_L'		, 'thigh_L_tail', 'shin_L_tail'),
	('Foot_ik_L'		, 'shin_L_tail', 'foot_L_tail'),
	('Toe_ik_L'		, 'foot_L_tail', 'toe_L_tail'),
	('UpLeg_L'		, 'thigh_root_L_tail', 'thigh_L_tail'),
	('LoLeg_L'		, 'thigh_L_tail', 'shin_L_tail'),
	('Foot_L'		, 'shin_L_tail', 'foot_L_tail'),
	('Toe_L'		, 'foot_L_tail', 'toe_L_tail'),

	('Hip_R'		, 'hip_tail', 'thigh_root_R_head'),
	('LegRoot_R'		, 'thigh_root_R_head', 'thigh_root_R_tail'),
	('UpLeg_fk_R'		, 'thigh_root_R_tail', 'thigh_R_tail'),
	('LoLeg_fk_R'		, 'thigh_R_tail', 'shin_R_tail'),
	('Foot_fk_R'		, 'shin_R_tail', 'foot_R_tail'),
	('Toe_fk_R'		, 'foot_R_tail', 'toe_R_tail'),
	('UpLeg_ik_R'		, 'thigh_root_R_tail', 'thigh_R_tail'),
	('LoLeg_ik_R'		, 'thigh_R_tail', 'shin_R_tail'),
	('Foot_ik_R'		, 'shin_R_tail', 'foot_R_tail'),
	('Toe_ik_R'		, 'foot_R_tail', 'toe_R_tail'),
	('UpLeg_R'		, 'thigh_root_R_tail', 'thigh_R_tail'),
	('LoLeg_R'		, 'thigh_R_tail', 'shin_R_tail'),
	('Foot_R'		, 'shin_R_tail', 'foot_R_tail'),
	('Toe_R'		, 'foot_R_tail', 'toe_R_tail'),

	('FootCtrl_L'		, 'footCtrl_L_head', 'footCtrl_L_tail'),
	('TipToe_L'		, 'tiptoe_L_head', 'tiptoe_L_tail'),
	('TumbleOut_L'		, 'tumble_out_L_head', 'tumble_out_L_tail'),
	('TumbleIn_L'		, 'tumble_in_L_head', 'tumble_in_L_tail'),
	('Heel_L'		, 'heel_L_head', 'heel_L_tail'),
	('RotateToe_L'		, 'rotate_toe_L_head', 'rotate_toe_L_tail'),
	('ToeTarget_L'		, 'toe_target_L_head', 'toe_target_L_tail'),
	('FootTarget_L'		, 'foot_target_L_head', 'foot_target_L_tail'),
	('LegTarget_L'		, 'leg_target_L_head', 'leg_target_L_tail'),
	('FootTumble_L'		, 'foot_tumble_L_head', 'foot_tumble_L_tail'),
	('FootRoll_L'		, 'foot_Roll_L_head', 'foot_Roll_L_tail'),
	('Knee_L'		, 'knee_L_head', 'knee_L_tail'),
	('ikfkFootCtrl_L'	, 'ikfk_foot_L_head', 'ikfk_foot_L_tail'),

	('FootCtrl_R'		, 'footCtrl_R_head', 'footCtrl_R_tail'),
	('TipToe_R'		, 'tiptoe_R_head', 'tiptoe_R_tail'),
	('TumbleOut_R'		, 'tumble_out_R_head', 'tumble_out_R_tail'),
	('TumbleIn_R'		, 'tumble_in_R_head', 'tumble_in_R_tail'),
	('Heel_R'		, 'heel_R_head', 'heel_R_tail'),
	('RotateToe_R'		, 'rotate_toe_R_head', 'rotate_toe_R_tail'),
	('ToeTarget_R'		, 'toe_target_R_head', 'toe_target_R_tail'),
	('FootTarget_R'		, 'foot_target_R_head', 'foot_target_R_tail'),
	('LegTarget_R'		, 'leg_target_R_head', 'leg_target_R_tail'),
	('FootTumble_R'		, 'foot_tumble_R_head', 'foot_tumble_R_tail'),
	('FootRoll_R'		, 'foot_Roll_R_head', 'foot_Roll_R_tail'),
	('Knee_R'		, 'knee_R_head', 'knee_R_tail'),
	('ikfkFootCtrl_R'	, 'ikfk_foot_R_head', 'ikfk_foot_R_tail'),

	('Breathe'		, 'spine1', 'chest-front'),
	('Stomach'		, 'chest-front', 'pelvis'),
	('ToungeBase'		, 'tounge-root', 'tounge-mid'),
	('ToungeTip'		, 'tounge-mid', 'tounge-tip'),

	('Eye_L'		, 'r-eye', 'r-eye-front'),
	('UpLid_L'		, 'r-eye', 'r-uplid'),
	('LoLid_L'		, 'r-eye', 'r-lolid'),
	('Gaze_L'		, 'gaze_L_head', 'gaze_L_tail'),
	('Eye_R'		, 'l-eye', 'l-eye-front'),
	('UpLid_R'		, 'l-eye', 'l-uplid'),
	('LoLid_R'		, 'l-eye', 'l-lolid'),
	('Gaze_R'		, 'gaze_R_head', 'gaze_R_tail'),
	('Gaze'			, 'gaze_head', 'gaze_tail'),

	('UpArmTwist_L'		, 'r-shoulder', 'r-elbow'),
	('LoArmTwist_L'		, 'r-elbow', 'r-hand'),
	('UpLegTwist_L'		, 'r-upper-leg', 'r-knee'),
	('UpArmTwist_R'		, 'l-shoulder', 'l-elbow'),
	('LoArmTwist_R'		, 'l-elbow', 'l-hand'),
	('UpLegTwist_R'		, 'l-upper-leg', 'l-knee'),
]

#	Flags
#

F_CON = 0x001
F_DEF = 0x002
F_RES = 0x004
F_WIR = 0x008
F_NOSCALE = 0x010

#
#	Bone layers
#

L_MAIN = 	0x0001
L_SKEL =	0x0002
L_ARMIK =	0x0004
L_ARMFK =	0x0008
L_LEGIK =	0x0010
L_LEGFK =	0x0020
L_HANDIK =	0x0040
L_HANDFK =	0x0080

L_PANEL	=	0x0100
L_HEAD =	0x0200
L_TOE =		0x0400

L_HLPIK	=	0x1000
L_HLPFK	=	0x2000
L_HELP	=	0x4000
L_DEF =		0x8000

armature = [
	('Root',		0.0, None, F_WIR, L_MAIN, (1,1,1)),

	('HandCtrl_L',	1.5708, 'Root', F_WIR, L_ARMIK, (1,1,1)),
	('HandCtrl_R',	-1.5708, 'Root', F_WIR, L_ARMIK, (1,1,1)),

	('Hips',		0.0, 'Root', F_DEF, L_MAIN+L_DEF, (1,1,1)),
	('Spine3',		0.0, 'Hips', F_DEF, L_MAIN+L_DEF, (1,1,1)),
	('Spine2',		0.0, 'Spine3', F_DEF+F_CON, L_MAIN+L_DEF, (1,1,1)),
	('Spine1',		0.0, 'Spine2', F_DEF+F_CON, L_MAIN+L_DEF, (1,1,1)),
	('Neck',		0.0, 'Spine1', F_DEF+F_CON+F_WIR, L_MAIN+L_DEF, (1,1,1)),
	('Head',		0.0, 'Neck', F_DEF+F_CON+F_WIR, L_MAIN+L_DEF, (1,1,1)),
	('Jaw',			0.0, 'Head', F_DEF+F_WIR, L_MAIN+L_DEF, (1,1,1)),

	('Clavicle_L',		1.5708, 'Spine1', F_DEF+F_WIR, L_SKEL+L_DEF, (1,1,1)),
	('ikfkHand_L',		-1.5708, 'Clavicle_L', F_WIR, L_MAIN+L_ARMIK+L_ARMFK, (1,1,1)),
	('ArmRoot_L',		1.5708, 'Clavicle_L', F_RES, L_SKEL, (0,0,2)),
	('Elbow_L',		0, 'ArmRoot_L', F_WIR,  L_ARMIK, (1,1,1)),
	('UpArm_L',		1.5708, 'ArmRoot_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,10)),
	('LoArm_L',		1.5708, 'UpArm_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,10)),
	('Hand_L',		1.5708, 'LoArm_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('UpArm_ik_L',		1.5708, 'ArmRoot_L', F_CON+F_RES, L_HLPIK, (0,0,10)),
	('LoArm_ik_L',		1.5708, 'UpArm_ik_L', F_CON+F_RES, L_HLPIK, (0,0,10)),
	('Hand_ik_L',		1.5708, 'LoArm_ik_L', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('FingerCurl_ik_L',	0, 'LoArm_ik_L', F_WIR, L_ARMIK, (1,1,1)),
	('UpArm_fk_L',		1.5708, 'ArmRoot_L', F_CON, L_ARMFK, (0,0,10)),
	('LoArm_fk_L',		1.5708, 'UpArm_fk_L', F_CON, L_ARMFK, (0,0,10)),
	('Hand_fk_L',		1.5708, 'LoArm_fk_L', F_CON+F_WIR, L_ARMFK, (1,1,1)),
	('FingerCurl_fk_L',	0, 'LoArm_fk_L', F_WIR, L_ARMFK, (1,1,1)),

	('Clavicle_R',		-1.5708, 'Spine1', F_DEF+F_WIR, L_SKEL+L_DEF, (1,1,1)),
	('ikfkHand_R',		-1.5708, 'Clavicle_R', F_WIR, L_MAIN+L_ARMIK+L_ARMFK, (1,1,1)),
	('ArmRoot_R',		-1.5708, 'Clavicle_R', F_RES, L_SKEL, (0,0,2)),
	('Elbow_R',		0, 'ArmRoot_R', F_WIR, L_ARMIK, (1,1,1)),
	('UpArm_R',		-1.5708, 'ArmRoot_R', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,10)),
	('LoArm_R',		-1.5708, 'UpArm_R', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,10)),
	('Hand_R',		-1.5708, 'LoArm_R', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('UpArm_ik_R',		-1.5708, 'ArmRoot_R', F_CON+F_RES, L_HLPIK, (0,0,10)),
	('LoArm_ik_R',		-1.5708, 'UpArm_ik_R', F_CON+F_RES, L_HLPIK, (0,0,10)),
	('Hand_ik_R',		-1.5708, 'LoArm_ik_R', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('FingerCurl_ik_R',	3.14158, 'LoArm_ik_R', F_WIR, L_MAIN+L_ARMIK, (1,1,1)),
	('UpArm_fk_R',		-1.5708, 'ArmRoot_R', F_CON, L_ARMFK, (0,0,10)),
	('LoArm_fk_R',		-1.5708, 'UpArm_fk_R', F_CON, L_ARMFK, (0,0,10)),
	('Hand_fk_R',		-1.5708, 'LoArm_fk_R', F_CON+F_WIR, L_ARMFK, (1,1,1)),
	('FingerCurl_fk_R',	-3.14158, 'LoArm_fk_R', F_WIR, L_ARMFK, (1,1,1)),

	('Finger-1-1_L',	1.5708, 'Hand_L', F_DEF+F_RES, L_DEF, (1,1,1)),
	('Finger-1-2_L',	1.5708, 'Finger-1-1_L', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-1-3_L',	1.5708, 'Finger-1-2_L', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-2-1_L',	1.5708, 'Hand_L', F_DEF+F_RES, L_DEF, (1,1,1)),
	('Finger-2-2_L',	1.5708, 'Finger-2-1_L', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-2-3_L',	1.5708, 'Finger-2-2_L', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-3-1_L',	1.5708, 'Hand_L', F_DEF+F_RES, L_DEF, (1,1,1)),
	('Finger-3-2_L',	1.5708, 'Finger-3-1_L', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-3-3_L',	1.5708, 'Finger-3-2_L', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-4-1_L',	1.5708, 'Hand_L', F_DEF+F_RES, L_DEF, (1,1,1)),
	('Finger-4-2_L',	1.5708, 'Finger-4-1_L', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-4-3_L',	1.5708, 'Finger-4-2_L', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-5-1_L',	1.5708, 'Hand_L', F_DEF+F_RES, L_DEF, (1,1,1)),
	('Finger-5-2_L',	1.5708, 'Finger-5-1_L', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-5-3_L',	1.5708, 'Finger-5-2_L', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),

	('Finger-1-1_fk_L',	1.5708, 'Hand_fk_L', 0, L_HANDFK, (1,1,1)),
	('Finger-1-2_fk_L',	1.5708, 'Finger-1-1_fk_L', F_CON, L_HANDFK, (1,1,1)),
	('Finger-1-3_fk_L',	1.5708, 'Finger-1-2_fk_L', F_CON, L_HANDFK, (1,1,1)),
	('Finger-2-1_fk_L',	1.5708, 'Hand_fk_L', 0, L_HANDFK, (1,1,1)),
	('Finger-2-2_fk_L',	1.5708, 'Finger-2-1_fk_L', F_CON, L_HANDFK, (1,1,1)),
	('Finger-2-3_fk_L',	1.5708, 'Finger-2-2_fk_L', F_CON, L_HANDFK, (1,1,1)),
	('Finger-3-1_fk_L',	1.5708, 'Hand_fk_L', 0, L_HANDFK, (1,1,1)),
	('Finger-3-2_fk_L',	1.5708, 'Finger-3-1_fk_L', F_CON, L_HANDFK, (1,1,1)),
	('Finger-3-3_fk_L',	1.5708, 'Finger-3-2_fk_L', F_CON, L_HANDFK, (1,1,1)),
	('Finger-4-1_fk_L',	1.5708, 'Hand_fk_L', 0, L_HANDFK, (1,1,1)),
	('Finger-4-2_fk_L',	1.5708, 'Finger-4-1_fk_L', F_CON, L_HANDFK, (1,1,1)),
	('Finger-4-3_fk_L',	1.5708, 'Finger-4-2_fk_L', F_CON, L_HANDFK, (1,1,1)),
	('Finger-5-1_fk_L',	1.5708, 'Hand_fk_L', 0, L_HANDFK, (1,1,1)),
	('Finger-5-2_fk_L',	1.5708, 'Finger-5-1_fk_L', F_CON, L_HANDFK, (1,1,1)),
	('Finger-5-3_fk_L',	1.5708, 'Finger-5-2_fk_L', F_CON, L_HANDFK, (1,1,1)),

	('Finger-1-1_ik_L',	1.5708, 'Hand_ik_L', 0, L_HANDIK, (1,1,1)),
	('Finger-1-2_ik_L',	1.5708, 'Finger-1-1_ik_L', F_CON, L_HANDIK, (1,1,1)),
	('Finger-1-3_ik_L',	1.5708, 'Finger-1-2_ik_L', F_CON, L_HANDIK, (1,1,1)),
	('Finger-2-1_ik_L',	1.5708, 'Hand_ik_L', 0, L_HANDIK, (1,1,1)),
	('Finger-2-2_ik_L',	1.5708, 'Finger-2-1_ik_L', F_CON, L_HANDIK, (1,1,1)),
	('Finger-2-3_ik_L',	1.5708, 'Finger-2-2_ik_L', F_CON, L_HANDIK, (1,1,1)),
	('Finger-3-1_ik_L',	1.5708, 'Hand_ik_L', 0, L_HANDIK, (1,1,1)),
	('Finger-3-2_ik_L',	1.5708, 'Finger-3-1_ik_L', F_CON, L_HANDIK, (1,1,1)),
	('Finger-3-3_ik_L',	1.5708, 'Finger-3-2_ik_L', F_CON, L_HANDIK, (1,1,1)),
	('Finger-4-1_ik_L',	1.5708, 'Hand_ik_L', 0, L_HANDIK, (1,1,1)),
	('Finger-4-2_ik_L',	1.5708, 'Finger-4-1_ik_L', F_CON, L_HANDIK, (1,1,1)),
	('Finger-4-3_ik_L',	1.5708, 'Finger-4-2_ik_L', F_CON, L_HANDIK, (1,1,1)),
	('Finger-5-1_ik_L',	1.5708, 'Hand_ik_L', 0, L_HANDIK, (1,1,1)),
	('Finger-5-2_ik_L',	1.5708, 'Finger-5-1_ik_L', F_CON, L_HANDIK, (1,1,1)),
	('Finger-5-3_ik_L',	1.5708, 'Finger-5-2_ik_L', F_CON, L_HANDIK, (1,1,1)),

	('Finger-1-1_R',	1.5708, 'Hand_R', F_DEF+F_RES, L_DEF, (1,1,1)),
	('Finger-1-2_R',	1.5708, 'Finger-1-1_R', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-1-3_R',	1.5708, 'Finger-1-2_R', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-2-1_R',	1.5708, 'Hand_R', F_DEF+F_RES, L_DEF, (1,1,1)),
	('Finger-2-2_R',	1.5708, 'Finger-2-1_R', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-2-3_R',	1.5708, 'Finger-2-2_R', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-3-1_R',	1.5708, 'Hand_R', F_DEF+F_RES, L_DEF, (1,1,1)),
	('Finger-3-2_R',	1.5708, 'Finger-3-1_R', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-3-3_R',	1.5708, 'Finger-3-2_R', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-4-1_R',	1.5708, 'Hand_R', F_DEF+F_RES, L_DEF, (1,1,1)),
	('Finger-4-2_R',	1.5708, 'Finger-4-1_R', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-4-3_R',	1.5708, 'Finger-4-2_R', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-5-1_R',	1.5708, 'Hand_R', F_DEF+F_RES, L_DEF, (1,1,1)),
	('Finger-5-2_R',	1.5708, 'Finger-5-1_R', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),
	('Finger-5-3_R',	1.5708, 'Finger-5-2_R', F_DEF+F_RES+F_CON, L_DEF, (1,1,1)),

	('Finger-1-1_fk_R',	1.5708, 'Hand_fk_R', 0, L_HANDFK, (1,1,1)),
	('Finger-1-2_fk_R',	1.5708, 'Finger-1-1_fk_R', F_CON, L_HANDFK, (1,1,1)),
	('Finger-1-3_fk_R',	1.5708, 'Finger-1-2_fk_R', F_CON, L_HANDFK, (1,1,1)),
	('Finger-2-1_fk_R',	1.5708, 'Hand_fk_R', 0, L_HANDFK, (1,1,1)),
	('Finger-2-2_fk_R',	1.5708, 'Finger-2-1_fk_R', F_CON, L_HANDFK, (1,1,1)),
	('Finger-2-3_fk_R',	1.5708, 'Finger-2-2_fk_R', F_CON, L_HANDFK, (1,1,1)),
	('Finger-3-1_fk_R',	1.5708, 'Hand_fk_R', 0, L_HANDFK, (1,1,1)),
	('Finger-3-2_fk_R',	1.5708, 'Finger-3-1_fk_R', F_CON, L_HANDFK, (1,1,1)),
	('Finger-3-3_fk_R',	1.5708, 'Finger-3-2_fk_R', F_CON, L_HANDFK, (1,1,1)),
	('Finger-4-1_fk_R',	1.5708, 'Hand_fk_R', 0, L_HANDFK, (1,1,1)),
	('Finger-4-2_fk_R',	1.5708, 'Finger-4-1_fk_R', F_CON, L_HANDFK, (1,1,1)),
	('Finger-4-3_fk_R',	1.5708, 'Finger-4-2_fk_R', F_CON, L_HANDFK, (1,1,1)),
	('Finger-5-1_fk_R',	1.5708, 'Hand_fk_R', 0, L_HANDFK, (1,1,1)),
	('Finger-5-2_fk_R',	1.5708, 'Finger-5-1_fk_R', F_CON, L_HANDFK, (1,1,1)),
	('Finger-5-3_fk_R',	1.5708, 'Finger-5-2_fk_R', F_CON, L_HANDFK, (1,1,1)),

	('Finger-1-1_ik_R',	1.5708, 'Hand_ik_R', 0, L_HANDIK, (1,1,1)),
	('Finger-1-2_ik_R',	1.5708, 'Finger-1-1_ik_R', F_CON, L_HANDIK, (1,1,1)),
	('Finger-1-3_ik_R',	1.5708, 'Finger-1-2_ik_R', F_CON, L_HANDIK, (1,1,1)),
	('Finger-2-1_ik_R',	1.5708, 'Hand_ik_R', 0, L_HANDIK, (1,1,1)),
	('Finger-2-2_ik_R',	1.5708, 'Finger-2-1_ik_R', F_CON, L_HANDIK, (1,1,1)),
	('Finger-2-3_ik_R',	1.5708, 'Finger-2-2_ik_R', F_CON, L_HANDIK, (1,1,1)),
	('Finger-3-1_ik_R',	1.5708, 'Hand_ik_R', 0, L_HANDIK, (1,1,1)),
	('Finger-3-2_ik_R',	1.5708, 'Finger-3-1_ik_R', F_CON, L_HANDIK, (1,1,1)),
	('Finger-3-3_ik_R',	1.5708, 'Finger-3-2_ik_R', F_CON, L_HANDIK, (1,1,1)),
	('Finger-4-1_ik_R',	1.5708, 'Hand_ik_R', 0, L_HANDIK, (1,1,1)),
	('Finger-4-2_ik_R',	1.5708, 'Finger-4-1_ik_R', F_CON, L_HANDIK, (1,1,1)),
	('Finger-4-3_ik_R',	1.5708, 'Finger-4-2_ik_R', F_CON, L_HANDIK, (1,1,1)),
	('Finger-5-1_ik_R',	1.5708, 'Hand_ik_R', 0, L_HANDIK, (1,1,1)),
	('Finger-5-2_ik_R',	1.5708, 'Finger-5-1_ik_R', F_CON, L_HANDIK, (1,1,1)),
	('Finger-5-3_ik_R',	1.5708, 'Finger-5-2_ik_R', F_CON, L_HANDIK, (1,1,1)),

	('Hip_L',		0.0, 'Hips', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('LegRoot_L',		0.0, 'Hip_L', F_CON+F_RES, L_SKEL, (0,0,2)),
	('UpLeg_L',		0.0, 'LegRoot_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,8)),
	('LoLeg_L',		0.0, 'UpLeg_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,5)),
	('Foot_L',		0.0, 'LoLeg_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('Toe_L',		0.0, 'Foot_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('UpLeg_ik_L',		0.0, 'LegRoot_L', F_CON+F_RES, L_HLPIK, (0,0,8)),
	('LoLeg_ik_L',		0.0, 'UpLeg_ik_L', F_CON+F_RES, L_HLPIK, (0,0,5)),
	('Foot_ik_L',		0.0, 'LoLeg_ik_L', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('Toe_ik_L',		0.0, 'Foot_ik_L', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('UpLeg_fk_L',		0.0, 'LegRoot_L', F_CON, L_LEGFK, (0,0,8)),
	('LoLeg_fk_L',		0.0, 'UpLeg_fk_L', F_CON, L_LEGFK, (0,0,5)),
	('Foot_fk_L',		0.0, 'LoLeg_fk_L', F_CON, L_LEGFK, (1,1,1)),
	('Toe_fk_L',		0.0, 'Foot_fk_L', F_CON, L_LEGFK, (1,1,1)),

	('Hip_R',		0.0, 'Hips', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('LegRoot_R',		0.0, 'Hip_R', F_CON+F_RES, L_SKEL, (0,0,2)),
	('UpLeg_R',		0.0, 'LegRoot_R', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,8)),
	('LoLeg_R',		0.0, 'UpLeg_R', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,5)),
	('Foot_R',		0.0, 'LoLeg_R', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('Toe_R',		0.0, 'Foot_R', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('UpLeg_ik_R',		0.0, 'LegRoot_R', F_CON+F_RES, L_HLPIK, (0,0,8)),
	('LoLeg_ik_R',		0.0, 'UpLeg_ik_R', F_CON+F_RES, L_HLPIK, (0,0,5)),
	('Foot_ik_R',		0.0, 'LoLeg_ik_R', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('Toe_ik_R',		0.0, 'Foot_ik_R', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('UpLeg_fk_R',		0.0, 'LegRoot_R', F_CON, L_LEGFK, (0,0,8)),
	('LoLeg_fk_R',		0.0, 'UpLeg_fk_R', F_CON, L_LEGFK, (0,0,5)),
	('Foot_fk_R',		0.0, 'LoLeg_fk_R', F_CON, L_LEGFK, (1,1,1)),
	('Toe_fk_R',		0.0, 'Foot_fk_R', F_CON, L_LEGFK, (1,1,1)),

	('FootCtrl_L',		0.0, 'Root', F_WIR, L_LEGIK, (1,1,1)),
	('TipToe_L',		0.0, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1)),
	('TumbleOut_L',		0.0, 'TipToe_L', F_RES, L_HELP, (1,1,1)),
	('TumbleIn_L',		0.0, 'TumbleOut_L', F_RES, L_HELP, (1,1,1)),
	('Heel_L',		0.0, 'TumbleIn_L', F_RES, L_HELP, (1,1,1)),
	('RotateToe_L',		0.0, 'Heel_L', F_WIR, L_LEGIK, (1,1,1)),
	('ToeTarget_L',		0.0, 'RotateToe_L', F_RES, L_HELP, (1,1,1)),
	('FootTarget_L',	0.0, 'Heel_L', F_RES, L_HELP, (1,1,1)),
	('LegTarget_L',		0.0, 'FootCtrl_L', F_RES, L_HELP, (1,1,1)),
	('FootTumble_L',	0.0, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1)),
	('FootRoll_L',		-1.5708, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1)),
	('Knee_L',		0.0, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1)),
	('ikfkFootCtrl_L',	-1.5708, 'FootCtrl_L', F_WIR, L_MAIN+L_LEGIK+L_LEGFK, (1,1,1)),

	('FootCtrl_R',		0.0, 'Root', F_WIR, L_LEGIK, (1,1,1)),
	('TipToe_R',		0.0, 'FootCtrl_R', F_WIR, L_LEGIK, (1,1,1)),
	('TumbleOut_R',		0.0, 'TipToe_R', F_RES, L_HELP, (1,1,1)),
	('TumbleIn_R',		0.0, 'TumbleOut_R', F_RES, L_HELP, (1,1,1)),
	('Heel_R',		0.0, 'TumbleIn_R', F_RES, L_HELP, (1,1,1)),
	('RotateToe_R',		0.0, 'Heel_R', F_WIR, L_LEGIK, (1,1,1)),
	('ToeTarget_R',		0.0, 'RotateToe_R', F_RES, L_HELP, (1,1,1)),
	('FootTarget_R',	0.0, 'Heel_R', F_RES, L_HELP, (1,1,1)),
	('LegTarget_R',		0.0, 'FootCtrl_R', F_RES, L_HELP, (1,1,1)),
	('FootTumble_R',	0.0, 'FootCtrl_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootRoll_R',		-1.5708, 'FootCtrl_R', F_WIR, L_LEGIK, (1,1,1)),
	('Knee_R',		0.0, 'FootCtrl_R', F_WIR, L_LEGIK, (1,1,1)),
	('ikfkFootCtrl_R',	-1.5708, 'FootCtrl_R', F_WIR, L_MAIN+L_LEGIK, (1,1,1)),

	('Breathe', 		0.0, 'Spine2', F_CON+F_DEF, L_DEF, (1,1,1)),
	('Stomach', 		0.0, 'Breathe', F_CON+F_DEF+F_NOSCALE+F_RES, L_DEF, (1,1,1)),
	('ToungeBase', 		0.0, 'Jaw', F_DEF+F_NOSCALE, L_DEF+L_HEAD, (1,1,1)),
	('ToungeTip', 		0.0, 'ToungeBase', F_DEF+F_CON+F_NOSCALE, L_DEF+L_HEAD, (1,1,1)),

	('Eye_L', 		0.0, 'Head', F_DEF+F_RES, L_DEF, (1,1,1)),
	('UpLid_L', 		0.0, 'Head', F_DEF+F_RES, L_DEF, (1,1,1)),
	('LoLid_L', 		0.0, 'Head', F_DEF+F_RES, L_DEF, (1,1,1)),
	('Eye_R', 		0.0, 'Head', F_DEF+F_RES, L_DEF, (1,1,1)),
	('UpLid_R', 		0.0, 'Head', F_DEF+F_RES, L_DEF, (1,1,1)),
	('LoLid_R', 		0.0, 'Head', F_DEF+F_RES, L_DEF, (1,1,1)),

	('Gaze', 		0.0, 'Root', 0, L_HEAD, (1,1,1)),
	('Gaze_L', 		0.0, 'Gaze', 0, L_HEAD, (1,1,1)),
	('Gaze_R', 		0.0, 'Gaze', 0, L_HEAD, (1,1,1)),

	('UpArmTwist_L', 	0.0, 'ArmRoot_L', F_CON+F_DEF+F_RES, L_DEF, (1,1,1)),
	('LoArmTwist_L', 	0.0, 'UpArm_L', F_CON+F_DEF+F_RES, L_DEF, (1,1,1)),
 	('UpLegTwist_L', 	0.0, 'LegRoot_L', F_CON+F_DEF+F_RES, L_DEF, (1,1,1)),
	('UpArmTwist_R', 	0.0, 'ArmRoot_R', F_CON+F_DEF+F_RES, L_DEF, (1,1,1)),
	('LoArmTwist_R', 	0.0, 'UpArm_R', F_CON+F_DEF+F_RES, L_DEF, (1,1,1)),
	('UpLegTwist_R', 	0.0, 'LegRoot_R', F_CON+F_DEF+F_RES, L_DEF, (1,1,1)),
]	

#
#	writeArmature(fp):
#	boolString(val):
#	addBone(bone, roll, parent, flags, layers, bbone, fp):
#

def writeArmature(fp):
	for (bone, roll, parent, flags, layers, bbone) in armature:
		addBone(bone, roll, parent, flags, layers, bbone, fp)
	return

def boolString(val):
	if val:
		return "True"
	else:
		return "False"

def addBone(bone, roll, parent, flags, layers, bbone, fp):
	conn = boolString(flags & F_CON)
	deform = boolString(flags & F_DEF)
	restr = boolString(flags & F_RES)
	wire = boolString(flags & F_WIR)
	scale = boolString(flags & F_NOSCALE == 0)
	(bin, bout, bseg) = bbone

	fp.write("\n  Bone %s \n" % (bone))
	(x, y, z) = mhxbones.boneHead[bone]
	fp.write("    head  %.6g %.6g %.6g  ;\n" % (x,-z,y))
	(x, y, z) = mhxbones.boneTail[bone]
	fp.write("    tail %.6g %.6g %.6g  ;\n" % (x,-z,y))
	if parent:
		fp.write("    parent Refer Bone %s ; \n" % (parent))
	fp.write(
"    roll %.6g ; \n" % (roll)+
"    bbone_in %d ; \n" % (bin) +
"    bbone_out %d ; \n" % (bout) +
"    bbone_segments %d ; \n" % (bseg) +
"    connected %s ; \n" % (conn) +
"    cyclic_offset True ; \n"+
"    deform %s ; \n" % (deform)+
"    hidden False ; \n"+
"    draw_wire %s ; \n" % (wire) +
"    hinge True ; \n"+
"    inherit_scale %s ; \n" % (scale) +
"    layer Array ")

	bit = 1
	for n in range(32):
		if layers & bit:
			fp.write("1 ")
		else:
			fp.write("0 ")
		bit = bit << 1

	fp.write(" ; \n" +
"    local_location True ; \n"+
"    locked False ; \n"+
"    multiply_vertexgroup_with_envelope False ; \n"+
"    restrict_select %s ; \n" % (restr) +
"  end Bone \n")

#
#	writeExtraPoses(fp):
#	poseFinger(fp, m, n, suffix):
#	poseFinger_fkik(fp, m, n, suffix, ik, curl):
#	poseIkConstraint(bone, subtar, chainlen, pole):
#

def writeExtraPoses(fp):
	for m in range(1,6):
		poseFinger(fp, m, 1, "L")
		poseFinger(fp, m, 1, "R")
		poseFinger_fkik(fp, m, 1, "L", "fk", False)
		poseFinger_fkik(fp, m, 1, "R", "fk", False)
		poseFinger_fkik(fp, m, 1, "L", "ik", False)
		poseFinger_fkik(fp, m, 1, "R", "ik", False)
		for n in range(2,4):
			poseFinger(fp, m, n, "L")
			poseFinger(fp, m, n, "R")
			poseFinger_fkik(fp, m, n, "L", "fk", True)
			poseFinger_fkik(fp, m, n, "R", "fk", True)
			poseFinger_fkik(fp, m, n, "L", "ik", True)
			poseFinger_fkik(fp, m, n, "R", "ik", True)

	poseIkConstraint(fp, "UpArmTwist_L", "LoArm_L", 1, None)
	poseIkConstraint(fp, "LoArmTwist_L", "Hand_L", 1, None)
	poseIkConstraint(fp, "UpLegTwist_L", "LoLeg_L", 1, None)
	poseIkConstraint(fp, "UpArmTwist_R", "LoArm_R", 1, None)
	poseIkConstraint(fp, "LoArmTwist_R", "Hand_R", 1, None)
	poseIkConstraint(fp, "UpLegTwist_R", "LoLeg_R", 1, None)

	poseIkConstraint(fp, "Eye_L", "Gaze_L", 1, None)
	poseIkConstraint(fp, "Eye_R", "Gaze_R", 1, None)
	poseIkConstraint(fp, "LoArmTwist_L", "Hand_L", 1, None)
	poseIkConstraint(fp, "UpLegTwist_L", "LoLeg_L", 1, None)

	return


def poseFinger(fp, m, n, suffix):
	fp.write(
"  Posebone Finger-%d-%d_%s \n" % (m, n, suffix) +
"    Constraint CopyRotIK COPY_ROTATION \n"+
"      target Refer Object HumanRig ; \n"+
"      invert Array 0 0 0  ; \n"+
"      use Array 1 1 1  ; \n"+
"      active False ; \n"+
"      expanded True ; \n"+
"      influence 1 ; \n"+
"      owner_space 'WORLD' ; \n"+
"      proxy_local False ; \n"+
"      subtarget 'Finger-%d-%d_ik_%s' ; \n" % (m, n, suffix) +
"      target_space 'WORLD' ; \n"+
"      use_offset False ; \n"+
"    end Constraint \n"+
"    Constraint CopyRotFK COPY_ROTATION \n"+
"      target Refer Object HumanRig ; \n"+
"      invert Array 0 0 0  ; \n"+
"      use Array 1 1 1  ; \n"+
"      active True ; \n"+
"      expanded True ; \n"+
"      influence 0 ; \n"+
"      owner_space 'WORLD' ; \n"+
"      proxy_local False ; \n"+
"      subtarget 'Finger-%d-%d_fk_%s' ; \n" % (m, n, suffix) +
"      target_space 'WORLD' ; \n"+
"      use_offset False ; \n"+
"    end Constraint \n"+
"    ik_dof Array 1 1 1  ; \n"+
"    ik_limit Array 0 0 0  ; \n"+
"    ik_max Array 3.14159274101 3.14159274101 3.14159274101  ; \n"+
"    ik_min Array -3.14159274101 -3.14159274101 -3.14159274101  ; \n"+
"    ik_stiffness Array 0.0 0.0 0.0  ; \n"+
"    # custom_shape Refer Object goboWidgetFinger_%s ; \n" % (suffix) + 
"    ik_lin_control False ; \n"+
"    ik_lin_weight 0 ; \n"+
"    ik_rot_control False ; \n"+
"    ik_rot_weight 0 ; \n"+
"    ik_stretch 0 ; \n"+
"    location (0,0,0) ; \n"+
"    lock_location Array 0 0 0  ; \n"+
"    lock_rotation Array 0 0 0  ; \n"+
"    lock_rotation_w False ; \n"+
"    lock_rotations_4d False ; \n"+
"    lock_scale Array 0 0 0  ; \n"+
"  end Posebone \n")

def poseFinger_fkik(fp, m, n, suffix, ik, curl):
	fp.write(
"  Posebone Finger-%d-%d_%s_%s \n" % (m, n, ik, suffix))
	if curl:
		fp.write(
"    Constraint Action ACTION \n"+
"      target Refer Object HumanRig ; \n"+
"      action Refer Action goboFingerCurl ; \n"+
"      active True ; \n"+
"      end_frame 21 ; \n"+
"      expanded True ; \n"+
"      influence 1 ; \n"+
"      maximum 0.1 ; \n"+
"      minimum -0.1 ; \n"+
"      owner_space 'WORLD' ; \n"+
"      proxy_local False ; \n"+
"      start_frame 1 ; \n"+
"      subtarget 'FingerCurl_%s_%s' ; \n" % (ik, suffix)+
"      target_space 'LOCAL' ; \n"+
"      transform_channel 'LOCATION_X' ; \n"+
"    end Constraint \n")
	fp.write(
"    ik_dof Array 1 1 1  ; \n"+
"    ik_limit Array 0 0 0  ; \n"+
"    ik_max Array 3.14159274101 3.14159274101 3.14159274101  ; \n"+
"    ik_min Array -3.14159274101 -3.14159274101 -3.14159274101  ; \n"+
"    ik_stiffness Array 0.0 0.0 0.0  ; \n"+
"    bone_group Refer BoneGroup %s ; \n" % (ik)+
"    # custom_shape Refer Object goboWidgetFinger_%s ; \n" % (suffix) +
"    ik_lin_control False ; \n"+
"    ik_lin_weight 0 ; \n"+
"    ik_rot_control False ; \n"+
"    ik_rot_weight 0 ; \n"+
"    ik_stretch 0 ; \n"+
"    location (0,0,0) ; \n"+
"    lock_location Array 1 1 1  ; \n"+
"    lock_rotation Array 1 1 0  ; \n"+
"    lock_rotation_w False ; \n"+
"    lock_rotations_4d False ; \n"+
"    lock_scale Array 1 1 1  ; \n"+
"  end Posebone \n")

def poseIkConstraint(fp, bone, subtar, chainlen, pole):
	fp.write("\n"+
"  Posebone %s\n" % bone +
"    Constraint IK IK\n" +
"      target Refer Object HumanRig ;\n" +
"      pos_lock Array 1 1 1  ;\n" +
"      rot_lock Array 1 1 1  ;\n" +
"      active True ;\n" +
"      axis_reference 'BONE' ;\n" +
"      chain_length %d ;\n" % chainlen +
"      expanded True ;\n" +
"      ik_type 'COPY_POSE' ;\n" +
"      influence 1 ;\n" +
"      iterations 500 ;\n" +
"      limit_mode 'LIMITDIST_INSIDE' ;\n" +
"      orient_weight 1 ;\n" +
"      owner_space 'WORLD' ;\n")

	if pole:
		(angle, ptar) = pole
		fp.write(
"      pole_angle %.6g ;\n" % angle +
"      pole_subtarget '%s' ;\n" % ptar +
"      pole_target Refer Object HumanRig ;\n")

	fp.write(
"      proxy_local False ;\n" +
"      subtarget '%s' ;\n" % subtar +
"      target_space 'WORLD' ;\n" +
"      use_position True ;\n" +
"      use_rotation False ;\n" +
"      use_stretch True ;\n" +
"      use_tail True ;\n" +
"      use_target True ;\n" +
"      weight 1 ;\n" +
"    end Constraint\n" +
"  end Posebone\n\n")

#
#	actionFingerCurl
#	actionFootTumble
#	actionFootRoll
#	writeActions(fp):
#	writeAction(name, action, ikfk, fp):
#	writeFCurves(name, (x01, y01, z01, w01), (x21, y21, z21, w21), fp):
#	writeFCurve(name, index, x01, x11, x21, fp):
#

actionFingerCurl = [
	("Finger-2-1", (0.923880, 0.0, 0.0, 0.382683), (0.793353, 0.0, 0.0, -0.608761) ), 
	("Finger-2-2", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-2-3", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-3-1", (0.923880, 0.0, 0.0, 0.382683), (0.793353, 0.0, 0.0, -0.608761) ), 
	("Finger-3-2", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-3-3", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-4-1", (0.923880, 0.0, 0.0, 0.382683), (0.793353, 0.0, 0.0, -0.608761) ), 
	("Finger-4-2", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-4-3", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-5-1", (0.923880, 0.0, 0.0, 0.382683), (0.793353, 0.0, 0.0, -0.608761) ), 
	("Finger-5-2", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-5-3", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
]

actionFootTumble = [
	("TumbleOut_L", (1.0, 0.0, 0.0, 0.0), (0.707107, 0.0, 0.0, -0.707107) ),
	("TumbleIn_L", (0.707107, 0.0, 0.0, 0.707107), (1.0, 0.0, 0.0, 0.0) ),
	("TumbleOut_R", (0.707107, 0.0, 0.0, 0.707107), (1.0, 0.0, 0.0, 0.0) ),
	("TumbleIn_R", (1.0, 0.0, 0.0, 0.0), (0.707107, 0.0, 0.0, -0.707107) ),
]

actionFootRoll = [
	("Heel_L", (0.707107, -0.707107, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0) ),
	("FootTarget_L", (1.0, 0.0, 0.0, 0.0), (0.707107, 0.707107, 0.0, 0.0) ),
	("Heel_R", (0.707107, -0.707107, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0) ),
	("FootTarget_R", (1.0, 0.0, 0.0, 0.0), (0.707107, 0.707107, 0.0, 0.0) ),
]


def writeActions(fp):
	writeAction("goboFingerCurl", actionFingerCurl, True, fp)
	writeAction("goboFootRoll", actionFootRoll, False, fp)
	writeAction("goboFootTumble", actionFootTumble, False, fp)
	return

def writeAction(name, action, ikfk, fp):
	fp.write("Action %s\n" % name)
	if ikfk:
		for (bone, (x01, y01, z01, w01), (x21, y21, z21, w21)) in action:
			writeFCurves("%s_ik_L" % bone, (x01, y01, z01, w01), (x21, y21, z21, w21), fp)
			writeFCurves("%s_ik_R" % bone, (x01, y01, z01, -w01), (x21, y21, z21, -w21), fp)
			writeFCurves("%s_fk_L" % bone, (x01, y01, z01, w01), (x21, y21, z21, w21), fp)
			writeFCurves("%s_fk_R" % bone, (x01, y01, z01, -w01), (x21, y21, z21, -w21), fp)
	else:
		for (bone, quat01, quat21) in action:
			writeFCurves(bone, quat01, quat21, fp)
	fp.write("end Action\n\n")
	return

def writeFCurves(name, (x01, y01, z01, w01), (x21, y21, z21, w21), fp):
	writeFCurve(name, 0, x01, 1.0, x21, fp)
	writeFCurve(name, 1, y01, 0.0, y21, fp)
	writeFCurve(name, 2, z01, 0.0, z21, fp)
	writeFCurve(name, 3, w01, 0.0, w21, fp)
	return

def writeFCurve(name, index, x01, x11, x21, fp):
	fp.write("\n" +
"  FCurve pose.pose_channels[\"%s\"].rotation_quaternion %d\n" % (name, index) +
"    kp 1 %.6g ;\n" % (x01) +
"    kp 11 %.6g ;\n" % (x11) +
"    kp 21 %.6g ;\n" % (x21) +
"    extrapolation 'CONSTANT' ;\n" +
"  end FCurve \n")
	return

#
#	constraintInfluences
#	writeConstraintDrivers(fp):
#

constraintInfluences = [
	("UpLeg_L", "CopyRotFK", "CopyRotIK", "ToggleLegIK"),
	("LoLeg_L", "CopyRotFK", "CopyRotIK", "ToggleLegIK"),
	("Foot_L", "CopyRotFK", "CopyRotIK", "ToggleLegIK"),
	("Toe_L", "CopyRotFK", "CopyRotIK", "ToggleLegIK"),
	("UpLeg_R", "CopyRotFK", "CopyRotIK", "ToggleLegIK"),
	("LoLeg_R", "CopyRotFK", "CopyRotIK", "ToggleLegIK"),
	("Foot_R", "CopyRotFK", "CopyRotIK", "ToggleLegIK"),
	("Toe_R", "CopyRotFK", "CopyRotIK", "ToggleLegIK"),

	("UpArm_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("LoArm_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Hand_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("UpArm_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("LoArm_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Hand_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),

	("Finger-1-1_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-1-2_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-1-3_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-2-1_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-2-2_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-2-3_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-3-1_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-3-2_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-3-3_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-4-1_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-4-2_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-4-3_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-5-1_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-5-2_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-5-3_L", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),

	("Finger-1-1_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-1-2_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-1-3_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-2-1_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-2-2_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-2-3_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-3-1_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-3-2_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-3-3_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-4-1_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-4-2_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-4-3_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-5-1_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-5-2_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
	("Finger-5-3_R", "CopyRotFK", "CopyRotIK", "ToggleArmIK"),
]

def writeConstraintDrivers(fp):
	for (bone, cnsFk, cnsIk, toggle) in constraintInfluences:
		fp.write("\n"+
"    FCurve pose.bones[\"%s\"].constraints[\"%s\"].influence 0\n" % (bone, cnsIk) +
"      Driver %s\n" % (toggle)+
"        expression '1.0' ;\n" +
"        show_debug_info False ;\n" +
"      end Driver\n" +
"    extrapolation 'CONSTANT' ;\n" +
"    end FCurve\n" +
"    FCurve pose.bones[\"%s\"].constraints[\"%s\"].influence 0\n" % (bone, cnsFk) +
"      Driver %s\n" % (toggle)+
"        expression '0.0' ;\n" +
"        show_debug_info False ;\n" +
"      end Driver\n" +
"    extrapolation 'CONSTANT' ;\n" +
"    end FCurve\n")
	return


