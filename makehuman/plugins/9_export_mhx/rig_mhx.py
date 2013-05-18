#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

MHX bone definitions 
"""

from collections import OrderedDict
from .flags import *
from . import posebone
from posebone import addPoseBone


Joints = [
    ('l-midfoot',           'l', ((0.5, 'l-ankle'), (0.5, 'l-foot-1'))),
    ('l-midtoe',            'l', ((0.5, 'l-foot-1'), (0.5, 'l-foot-2'))),
    ('r-midfoot',           'l', ((0.5, 'r-ankle'), (0.5, 'r-foot-1'))),
    ('r-midtoe',            'l', ((0.5, 'r-foot-1'), (0.5, 'r-foot-2'))),

    ('l-heel0',             'v', 12815),
    ('l-heel',              'l', ((-2.5,'l-foot-2'), (3.5,'l-foot-1'))),
    ('r-heel0',             'v', 6218),
    ('r-heel',              'l', ((-2.5,'r-foot-2'), (3.5,'r-foot-1'))),

    ('l-ankle-tip',         'o', ('l-ankle', (0,0,-1))),
    ('r-ankle-tip',         'o', ('r-ankle', (0,0,-1))),
    
    ('l-knee-pt',           'o', ('l-knee', [0,0,3])),
    ('r-knee-pt',           'o', ('r-knee', [0,0,3])),
    ('l-elbow-pt',          'o', ('l-elbow', [0,0,-3])),
    ('r-elbow-pt',          'o', ('r-elbow', [0,0,-3])),
]

HeadsTails = [
    # Hip = leg location
    ('leg_root.L',          'l-upperleg', ('l-upperleg', ysmall)),
    ('leg_root.R',          'r-upperleg', ('r-upperleg', ysmall)),
    
    # IK Leg
    ('ankle.L',         'l-ankle', 'l-ankle-tip'),
    ('ankle.ik.L',       'l-ankle', 'l-ankle-tip'),
    ('leg.ik.L',         'l-heel', 'l-foot-2'),
    ('toe.rev.L',        'l-foot-2', 'l-foot-1'),
    ('foot.rev.L',       'l-foot-1', 'l-ankle'),

    ('ankle.R',         'r-ankle', 'r-ankle-tip'),
    ('ankle.ik.R',       'r-ankle', 'r-ankle-tip'),
    ('leg.ik.R',         'r-heel', 'r-foot-2'),
    ('toe.rev.R',        'r-foot-2', 'r-foot-1'),
    ('foot.rev.R',       'r-foot-1', 'r-ankle'),

    # Pole Targets
    ('knee.pt.ik.L',     'l-knee-pt', ('l-knee-pt', ysmall)),
    ('knee.pt.fk.L',      'l-knee-pt', ('l-knee-pt', ysmall)),
    ('knee.link.L',    'l-knee', 'l-knee-pt'),
    ('FootPT_L',        ('l-midfoot', (0,1,0.2)), ('l-midfoot', (0,1.3,0.2))),
    ('ToePT_L',         ('l-midtoe', (0,1,0)), ('l-midtoe', (0,1.3,0))),

    ('knee.pt.ik.R',        'r-knee-pt', ('r-knee-pt', ysmall)),
    ('knee.pt.fk.R',      'r-knee-pt', ('r-knee-pt', ysmall)),
    ('knee.link.R',    'r-knee', 'r-knee-pt'),
    ('FootPT_R',        ('r-midfoot', (0,1,0.2)), ('r-midfoot', (0,1.3,0.2))),
    ('ToePT_R',         ('r-midtoe', (0,1,0)), ('r-midtoe', (0,1.3,0))),

    # Arm

    ('arm_root.L',       'l-shoulder', ('l-shoulder', ysmall)),
    ('arm_socket.L',     'l-shoulder', ('l-shoulder', ysmall)),
    ('arm_hinge.L',      'l-shoulder', ('l-shoulder', ysmall)),

    ('arm_root.R',       'r-shoulder', ('r-shoulder', ysmall)),
    ('arm_socket.R',     'r-shoulder', ('r-shoulder', ysmall)),
    ('arm_hinge.R',      'r-shoulder', ('r-shoulder', ysmall)),

    ('wrist.ik.L',             'l-hand', 'l-hand-end'),
    ('elbow.pt.ik.L',     'l-elbow-pt', ('l-elbow-pt', ysmall)),
    ('elbow.pt.fk.L',      'l-elbow-pt', ('l-elbow-pt', ysmall)),
    ('elbow.link.L',    'l-elbow', 'l-elbow-pt'),

    ('wrist.ik.R',             'r-hand', 'r-hand-end'),
    ('elbow.pt.ik.R',        'r-elbow-pt', ('r-elbow-pt', ysmall)),
    ('elbow.pt.fk.R',      'r-elbow-pt', ('r-elbow-pt', ysmall)),
    ('elbow.link.R',    'r-elbow', 'r-elbow-pt'),

]

"""
    # Directions    
    ('DirUpLegFwd_L',     'l-upperleg', ('l-upperleg', (0,0,1))),
    ('DirUpLegFwd_R',     'r-upperleg', ('r-upperleg', (0,0,1))),
    ('DirUpLegBack_L',    'l-upperleg', ('l-upperleg', (0,0,-1))),
    ('DirUpLegBack_R',    'r-upperleg', ('r-upperleg', (0,0,-1))),
    ('DirUpLegOut_L',     'l-upperleg', ('l-upperleg', (1,0,0))),
    ('DirUpLegOut_R',     'r-upperleg', ('r-upperleg', (-1,0,0))),

    ('DirKneeBack_L',     'l-knee', ('l-knee', (0,0,-1))),
    ('DirKneeBack_R',     'r-knee', ('r-knee', (0,0,-1))),
    ('DirKneeInv_L',      'l-knee', ('l-knee', (0,1,0))),
    ('DirKneeInv_R',      'r-knee', ('r-knee', (0,1,0))),
"""


Armature = OrderedDict([
    
    # Leg
    
    ('leg_root.L',      (0, 'hip.L', F_WIR, L_TWEAK, NoBB)),
    ('leg.ik.L',        (0, None, F_WIR, L_LLEGIK, NoBB)),
    ('toe.rev.L',       (0, 'leg.ik.L', F_WIR, L_LLEGIK, NoBB)),
    ('foot.rev.L',      (0, 'toe.rev.L', F_WIR, L_LLEGIK, NoBB)),
    ('ankle.L',         (0, None, F_WIR, L_LEXTRA, NoBB)),
    ('ankle.ik.L',      (0, 'foot.rev.L', 0, L_HELP2, NoBB)),

    ('leg_root.R',      (0, 'hip.R', F_WIR, L_TWEAK, NoBB)),
    ('leg.ik.R',        (0, None, F_WIR, L_RLEGIK, NoBB)),
    ('toe.rev.R',       (0, 'leg.ik.R', F_WIR, L_RLEGIK, NoBB)),
    ('foot.rev.R',      (0, 'toe.rev.R', F_WIR, L_RLEGIK, NoBB)),
    ('ankle.R',         (0, None, F_WIR, L_REXTRA, NoBB)),
    ('ankle.ik.R',      (0, 'foot.rev.R', 0, L_HELP2, NoBB)),

    ('knee.pt.ik.L',    (0, 'foot.rev.L', F_WIR, L_LLEGIK+L_LEXTRA, NoBB)),
    ('knee.pt.fk.L',    (0, 'thigh.L', 0, L_HELP2, NoBB)),
    ('knee.link.L',     (0, 'thigh.L', F_RES, L_LLEGIK+L_LEXTRA, NoBB)),

    ('knee.pt.ik.R',    (0, 'foot.rev.R', F_WIR, L_RLEGIK+L_REXTRA, NoBB)),
    ('knee.pt.fk.R',    (0, 'thigh.R', 0, L_HELP2, NoBB)),
    ('knee.link.R',     (0, 'thigh.R', F_RES, L_RLEGIK+L_REXTRA, NoBB)),

    # Arm
    
    ('arm_root.L',      (0, 'shoulder.L', F_WIR, L_TWEAK, NoBB)),
    ('arm_root.R',      (0, 'shoulder.R', F_WIR, L_TWEAK, NoBB)),
    ('arm_socket.L',    (0, 'hips', 0, L_HELP, NoBB)),
    ('arm_socket.R',    (0, 'hips', 0, L_HELP, NoBB)),
    ('arm_hinge.L',     (0, 'arm_socket.L', 0, L_HELP, NoBB)),
    ('arm_hinge.R',     (0, 'arm_socket.R', 0, L_HELP, NoBB)),

    ('wrist.ik.L',      (0, None, F_WIR, L_LARMIK, NoBB)),
    ('elbow.pt.ik.L',   (0, 'shoulder.L', F_WIR, L_LARMIK+L_LEXTRA, NoBB)),
    ('elbow.pt.fk.L',   (0, 'upper_arm.L', 0, L_HELP2, NoBB)),
    ('elbow.link.L',    (0, 'upper_arm.L', F_RES, L_LARMIK+L_LEXTRA, NoBB)),

    ('wrist.ik.R',      (0, None, F_WIR, L_RARMIK, NoBB)),
    ('elbow.pt.ik.R',   (0, 'shoulder.R', F_WIR, L_RARMIK+L_REXTRA, NoBB)),
    ('elbow.pt.fk.R',   (0, 'upper_arm.R', 0, L_HELP2, NoBB)),
    ('elbow.link.R',    (0, 'upper_arm.R', F_RES, L_RARMIK+L_REXTRA, NoBB)),
])

"""

    # Directions
    ('DirUpLegFwd_L',       180*D, 'leg_root.L', 0, L_HELP, NoBB)),
    ('DirUpLegFwd_R',       180*D, 'leg_root.R', 0, L_HELP, NoBB)),
    ('DirUpLegBack_L',      0*D, 'leg_root.L', 0, L_HELP, NoBB)),
    ('DirUpLegBack_R',      0*D, 'leg_root.R', 0, L_HELP, NoBB)),
    ('DirUpLegOut_L',       -90*D, 'leg_root.L', 0, L_HELP, NoBB)), 
    ('DirUpLegOut_R',       90*D, 'leg_root.R', 0, L_HELP, NoBB)),

    ('DirKneeBack_L',       0*D, 'thigh.L', 0, L_HELP, NoBB)),
    ('DirKneeBack_R',       0*D, 'thigh.R', 0, L_HELP, NoBB)),
    ('DirKneeInv_L',        0*D, 'thigh.L', 0, L_HELP, NoBB)),
    ('DirKneeInv_R',        0*D, 'thigh.R', 0, L_HELP, NoBB)),
"""

Parents = {
    'upper_arm.L' :     'arm_hinge.L',
    'upper_arm.R' :     'arm_hinge.R',
    'thigh.L' :         'leg_root.L',
    'thigh.R' :         'leg_root.R',    
}


RotationLimits = {
    # Leg
    
    'foot.rev.L' :   (-20*D,60*D, 0,0, 0,0),
    'foot.rev.R' :   (-20*D,60*D, 0,0, 0,0),
    'toe.rev.L' :    (-10*D,45*D, 0,0, 0,0),
    'toe.rev.R' :    (-10*D,45*D, 0,0, 0,0),
}

CustomShapes = {
    'master' :          'GZM_Root',

    # Leg
    
    'leg_root.L' :      'GZM_Ball025',
    'leg_root.R' :      'GZM_Ball025',
    'foot.rev.L' :      'GZM_RevFoot',
    'foot.rev.R' :      'GZM_RevFoot',
    'toe.rev.L' :       'GZM_RevToe',
    'toe.rev.R' :       'GZM_RevToe',
    'ankle.L' :         'GZM_Ball025',
    'ankle.R' :         'GZM_Ball025',
    'knee.pt.ik.L' :    'GZM_Cube025',
    'knee.pt.ik.R' :    'GZM_Cube025',

    # Arm
    
    'arm_root.L' :      'GZM_Ball025',
    'arm_root.R' :      'GZM_Ball025',
    'wrist.L' :         'GZM_Ball025',
    'wrist.R' :         'GZM_Ball025',
    'elbow.pt.ik.L' :   'GZM_Cube025',
    'elbow.pt.ik.R' :   'GZM_Cube025',
}


Hint = 18*D

Constraints = {
    #Leg
    
    'shin.ik.L' :   [
        ('LimitRot', C_OW_LOCAL, 1, ['Hint', (Hint,Hint, 0,0, 0,0), (1,0,0)])
        ],
    'shin.ik.R' :   [
        ('LimitRot', C_OW_LOCAL, 1, ['Hint', (Hint,Hint, 0,0, 0,0), (1,0,0)])
        ],        
    'ankle.ik.L' : [
        ('CopyLoc', 0, 1, ['Foot', 'foot.rev.L', (1,1,1), (0,0,0), 1, False]),
        ('CopyLoc', 0, 0, ['Ankle', 'ankle.L', (1,1,1), (0,0,0), 0, False]) 
        ],
    'ankle.ik.R' :  [
        ('CopyLoc', 0, 1, ['Foot', 'foot.rev.R', (1,1,1), (0,0,0), 1, False]),
        ('CopyLoc', 0, 0, ['Ankle', 'ankle.R', (1,1,1), (0,0,0), 0, False]) 
        ],
    'knee.link.L' : [
        ('StretchTo', 0, 1, ['Stretch', 'knee.pt.ik.L', 0, 1, 3.0])
        ],
    'knee.link.R' : [
        ('StretchTo', 0, 1, ['Stretch', 'knee.pt.ik.R', 0, 1, 3.0])
        ],

    #Arm
    
    'arm_socket.L' : [
        ('CopyLoc', 0, 1, ['Location', 'arm_root.L', (1,1,1), (0,0,0), 0, False]),
        ('CopyTrans', 0, 0, ['Hinge', 'arm_root.L', 0])
        ],        
    'arm_socket.R' : [
        ('CopyLoc', 0, 1, ['Location', 'arm_root.R', (1,1,1), (0,0,0), 0, False]),
        ('CopyTrans', 0, 0, ['Hinge', 'arm_root.R', 0])
        ],        
    'forearm.ik.L' :   [
        ('LimitRot', C_OW_LOCAL, 1, ['Hint', (Hint,Hint, 0,0, 0,0), (1,0,0)])
        ],
    'forearm.ik.R' :   [
        ('LimitRot', C_OW_LOCAL, 1, ['Hint', (Hint,Hint, 0,0, 0,0), (1,0,0)])
        ],        
    'elbow.link.L' : [
        ('StretchTo', 0, 1, ['Stretch', 'elbow.pt.ik.L', 0, 1, 3.0])
        ],
    'elbow.link.R' : [
        ('StretchTo', 0, 1, ['Stretch', 'elbow.pt.ik.R', 0, 1, 3.0])
        ],

}


#
#   PropLRDrivers
#   (Bone, Name, Props, Expr)
#

PropLRDrivers = [
    ('UpLeg', 'LegIK', ['LegIk'], 'x1'),
    ('LoLeg', 'LegIK', ['LegIk'], 'x1'),
    ('Foot', 'RevIK', ['LegIk', 'LegIkToAnkle'], 'x1*(1-x2)'),
    ('Foot', 'FreeIK', ['LegIk'], '1-x1'),
    ('Toe', 'RevIK', ['LegIk', 'LegIkToAnkle'], 'x1*(1-x2)'),
    ('LegIK', 'DistHip', ['LegStretch'], '1-x1'),
]

SoftPropLRDrivers = [
    #('KneePT', 'Foot', ['KneeFollowsFoot'], 'x1'),
    #('KneePT', 'Hip', ['KneeFollowsHip', 'KneeFollowsFoot'], 'x1*(1-x2)'),  
    ('AnkleIK', 'Foot', ['LegIkToAnkle'], '1-x1'),
    ('AnkleIK', 'Ankle', ['LegIkToAnkle'], 'x1'),
]

PropDrivers = [
    ('thigh.L', 'LimitRot', ['RotationLimits', 'LegIk_L'], 'x1*(1-x2)'),
    ('LoLeg_L', 'LimitRot', ['RotationLimits', 'LegIk_L'], 'x1*(1-x2)'),    
    ('Foot_L', 'LimitRot', ['RotationLimits', 'LegIk_L'], 'x1*(1-x2)'),    

    ('thigh.R', 'LimitRot', ['RotationLimits', 'LegIk-R'], 'x1*(1-x2)'),
    ('LoLeg_R', 'LimitRot', ['RotationLimits', 'LegIk_R'], 'x1*(1-x2)'),    
    ('Foot_R', 'LimitRot', ['RotationLimits', 'LegIk_R'], 'x1*(1-x2)'),    
]

#
#   DeformDrivers
#   Bone : (constraint, driver, rotdiff, keypoints)
#

DeformDrivers = []

#
#   ShapeDrivers
#   Shape : (driver, rotdiff, keypoints)
#

ShapeDrivers = {
}

expr90 = "%.3f*(1-%.3f*x1)" % (90.0/90.0, 2/pi)
expr70 = "%.3f*(1-%.3f*x1)" % (90.0/70.0, 2/pi)
expr60 = "%.3f*(1-%.3f*x1)" % (90.0/60.0, 2/pi)
expr45 = "%.3f*(1-%.3f*x1)" % (90.0/45.0, 2/pi)
expr90_90 = "%.3f*max(1-%.3f*x1,0)*max(1-%.3f*x2,0)" % (90.0/90.0, 2/pi, 2/pi)


HipTargetDrivers = []
"""
    ("legs-forward-90", "LR", expr90,
        [("UpLegVec", "DirUpLegFwd")]),
    ("legs-back-60", "LR", expr60,
        [("UpLegVec", "DirUpLegBack")]),
    ("legs-out-90", "LR", expr90_90,
        [("UpLegVec", "DirUpLegOut"),
         ("UpLeg", "UpLegVec")]),
    ("legs-out-90-neg-90", "LR", expr90_90,
        [("UpLegVec", "DirUpLegOut"),
         ("UpLeg", "UpLegVecNeg")]),
]
"""
KneeTargetDrivers = [
#    ("lolegs-back-90", "LR", expr90,
#        [("LoLeg", "DirKneeBack")]),
#    ("lolegs-back-135", "LR", expr45,
#        [("LoLeg", "DirKneeInv")]),
]


