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

Face bone definitions 
"""

from .flags import *
from . import posebone
from posebone import addPoseBone

Joints = [
    ('head-end',        'l', ((2.0, 'head'), (-1.0, 'neck'))),
    ('l-mouth',         'v', 11942),
    ('r-mouth',         'v', 5339),

    ('eyes',            'l', ((0.5, 'r-eye'), (0.5,'l-eye'))),
    ('gaze',            'o', ('eyes', (0,0,5))),
]

eyeOffs = (0,0,0.3)

HeadsTails = {
    'jaw' :             ('mouth', 'jaw'),
    'tongue_base' :     ('tongue-1', 'tongue-2'),
    'tongue_mid' :      ('tongue-2', 'tongue-3'),
    'tongue_tip' :      ('tongue-3', 'tongue-4'),

    'eye.R' :           ('r-eye', ('r-eye', eyeOffs)),
    'eye_parent.R' :    ('r-eye', ('r-eye', eyeOffs)),
    'up_lid.R' :        ('r-eye', 'r-upperlid'),
    'lo_lid.R' :        ('r-eye', 'r-lowerlid'),
   
    'eye.L' :           ('l-eye', ('l-eye', eyeOffs)),
    'eye_parent.L' :    ('l-eye', ('l-eye', eyeOffs)),
    'up_lid.L' :        ('l-eye', 'l-upperlid'),
    'lo_lid.L' :        ('l-eye', 'l-lowerlid'),

    'eyes' :            ('eyes', ('eyes', (0,0,1))),
    'gaze' :            ('gaze', ('gaze', (0,0,1))),
    'gaze_parent' :     ('head', 'head-2'),
}


Armature = {
    'jaw' :             (0, 'head', F_DEF, L_HEAD),
    'tongue_base' :     (0, 'jaw', F_DEF, L_HEAD),
    'tongue_mid' :      (0, 'tongue_base', F_DEF, L_HEAD),
    'tongue_tip' :      (0, 'tongue_mid', F_DEF, L_HEAD),
    'gaze_parent' :     (0, None, 0, L_HELP),
    'gaze' :            (180*D, 'gaze_parent', 0, L_HEAD),
    'eyes' :            (0, 'head', 0, L_HELP),
    'eye_parent.R' :    (0, 'head', 0, L_HELP),
    'eye_parent.L' :    (0, 'head', 0, L_HELP),
    'eye.R' :           (0, 'eye_parent.R', F_DEF, L_HEAD),
    'eye.L' :           (0, 'eye_parent.L', F_DEF, L_HEAD),
    'up_lid.R' :        (0.279253, 'head', F_DEF, L_HEAD),
    'lo_lid.R' :        (0, 'head', F_DEF, L_HEAD),
    'up_lid.L' :        (-0.279253, 'head', F_DEF, L_HEAD),
    'lo_lid.L' :        (0, 'head', F_DEF, L_HEAD),
}


CustomShapes = {
    'jaw' :     'GZM_Jaw',
    'gaze' :    'GZM_Gaze',
    'eye.R' :   'GZM_Circle025',
    'eye.L' :   'GZM_Circle025',
}


RotationLimits = {
    'jaw' : (-5*D,45*D, 0,0, -20*D,20*D),
}


Constraints = {
    'gaze_parent' : [
         ('CopyTrans', 0, 1, ['head', 'head', 0])
         ],
    'eyes' : [
        ('IK', 0, 1, ['IK', 'gaze', 1, None, (True, False,False), 1.0])
        ],
    'eye_parent.L' : [
        ('CopyRot', C_LOCAL, 1, ['eyes', 'eyes', (1,1,1), (0,0,0), True])
        ],
    'eye_parent.R' : [
        ('CopyRot', C_LOCAL, 1, ['eyes', 'eyes', (1,1,1), (0,0,0), True])
        ],
}

#
#    DeformDrivers(fp, amt):
#

def DeformDrivers(fp, amt):
    return []
    lidBones = [
    ('DEF_up_lid.L', 'PUpLid_L', (0, 40*D)),
    ('DEF_lo_lid.L', 'PLoLid_L', (0, 20*D)),
    ('DEF_up_lid.R', 'PUpLid_R', (0, 40*D)),
    ('DEF_lo_lid.R', 'PLoLid_R', (0, 20*D)),
    ]

    drivers = []
    for (driven, driver, coeff) in lidBones:
        drivers.append(    (driven, 'ROTQ', 'AVERAGE', None, 1, coeff,
         [("var", 'TRANSFORMS', [('OBJECT', amt.name, driver, 'LOC_Z', C_LOC)])]) )
    return drivers

#
#   PropDrivers
#   (Bone, Name, Props, Expr)
#

PropDrivers = [
    ('gaze_parent', 'head', ['GazeFollowsHead'], 'x1'),
]

