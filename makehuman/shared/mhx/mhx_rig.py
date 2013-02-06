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

Functions shared by all rigs 

Limit angles from http://hippydrome.com/
"""

import aljabr
from aljabr import *
import math
import os
import sys
import mh2proxy
import armature
import read_shapekeys
import log


from .mhx_globals import *
from . import mhxbones
from . import posebone
from . import mhx_custom
from . import read_rig

from . import rig_joints_25
from . import rig_body_25
from . import rig_shoulder_25
from . import rig_arm_25
from . import rig_finger_25
from . import rig_leg_25
from . import rig_toe_25
from . import rig_face_25
from . import rig_panel_25
from . import rig_skirt_25
from . import rigify_rig

        
def newSetupJoints (info, joints):
    info.locations = {}
    for (key, typ, data) in joints:
        #print(key)
        if typ == 'j':
            loc = mh2proxy.calcJointPos(info.mesh, data)
            info.locations[key] = loc
            info.locations[data] = loc
        elif typ == 'v':
            v = int(data)
            info.locations[key] = info.mesh.verts[v].co
        elif typ == 'x':
            info.locations[key] = [float(data[0]), float(data[2]), -float(data[1])]
        elif typ == 'vo':
            v = int(data[0])
            loc = info.mesh.verts[v].co
            info.locations[key] = [loc[0]+float(data[1]), loc[1]+float(data[3]), loc[2]-float(data[2])]
        elif typ == 'vl':
            ((k1, v1), (k2, v2)) = data
            loc1 = info.mesh.verts[int(v1)].co
            loc2 = info.mesh.verts[int(v2)].co
            info.locations[key] = vadd(vmul(loc1, k1), vmul(loc2, k2))
        elif typ == 'f':
            (raw, head, tail, offs) = data
            rloc = info.locations[raw]
            hloc = info.locations[head]
            tloc = info.locations[tail]
            #print(raw, rloc)
            vec = aljabr.vsub(tloc, hloc)
            vec2 = aljabr.vdot(vec, vec)
            vraw = aljabr.vsub(rloc, hloc)
            x = aljabr.vdot(vec, vraw) / vec2
            rvec = aljabr.vmul(vec, x)
            nloc = aljabr.vadd(hloc, rvec, offs)
            #print(key, nloc)
            info.locations[key] = nloc
        elif typ == 'b':
            info.locations[key] = info.locations[data]
        elif typ == 'p':
            x = info.locations[data[0]]
            y = info.locations[data[1]]
            z = info.locations[data[2]]
            info.locations[key] = [x[0],y[1],z[2]]
        elif typ == 'vz':
            v = int(data[0])
            z = info.mesh.verts[v].co[2]
            loc = info.locations[data[1]]
            info.locations[key] = [loc[0],loc[1],z]
        elif typ == 'X':
            r = info.locations[data[0]]
            (x,y,z) = data[1]
            r1 = [float(x), float(y), float(z)]
            info.locations[key] = aljabr.vcross(r, r1)
        elif typ == 'l':
            ((k1, joint1), (k2, joint2)) = data
            info.locations[key] = vadd(vmul(info.locations[joint1], k1), vmul(info.locations[joint2], k2))
        elif typ == 'o':
            (joint, offsSym) = data
            if type(offsSym) == str:
                offs = info.locations[offsSym]
            else:
                offs = offsSym
            info.locations[key] = vadd(info.locations[joint], offs)
        else:
            raise NameError("Unknown %s" % typ)
    return


def moveOriginToFloor(info):
    if info.config.feetonground:
        info.origin = info.locations['floor']
        for key in info.locations.keys():
            info.locations[key] = aljabr.vsub(info.locations[key], info.origin)
    else:
        info.origin = [0,0,0]
    return


def setupHeadsTails(info, headsTails):
    info.rigHeads = {}
    info.rigTails = {}
    for (bone, head, tail) in headsTails:
        info.rigHeads[bone] = findLocation(info, head)
        info.rigTails[bone] = findLocation(info, tail)
    return 


def findLocation(info, joint):
    try:
        (bone, offs) = joint
    except:
        offs = 0
    if offs:
        return vadd(info.locations[bone], offs)
    else:
        return info.locations[joint]


def writeArmature(fp, info, boneList):
    if info.config.mhx25:
        for (bone, roll, parent, flags, layers, bbone) in boneList:
            addBone25(info, bone, True, roll, parent, flags, layers, bbone, fp)
    else:
        for (bone, roll, parent, flags, layers, bbone) in boneList:
            addBone24(info, bone, True, roll, parent, flags, layers, bbone, fp)
    return


def addBone25(info, bone, cond, roll, parent, flags, layers, bbone, fp):
    conn = (flags & F_CON != 0)
    deform = (flags & F_DEF != 0)
    restr = (flags & F_RES != 0)
    wire = (flags & F_WIR != 0)
    lloc = (flags & F_NOLOC == 0)
    lock = (flags & F_LOCK != 0)
    cyc = (flags & F_NOCYC == 0)

    fp.write("\n  Bone %s %s\n" % (bone, cond))
    (x, y, z) = info.rigHeads[bone]
    fp.write("    head  %.6g %.6g %.6g  ;\n" % (x,-z,y))
    (x, y, z) = info.rigTails[bone]
    fp.write("    tail %.6g %.6g %.6g  ;\n" % (x,-z,y))
    if type(parent) == tuple:
        (soft, hard) = parent
        if hard:
            fp.write(
"#if toggle&T_HardParents\n" +
"    parent Refer Bone %s ;\n" % hard +
"#endif\n")
        if soft:
            fp.write(
"#if toggle&T_HardParents==0\n" +
"    parent Refer Bone %s ;\n" % soft +
"#endif\n")
    elif parent:
        fp.write("    parent Refer Bone %s ; \n" % (parent))
    fp.write(
"    roll %.6g ; \n" % (roll)+
"    use_connect %s ; \n" % (conn) +
"    use_deform %s ; \n" % (deform) +
"    show_wire %s ; \n" % (wire))

    if 1 and (flags & F_HID):
        fp.write("    hide True ; \n")

    if bbone:
        (bin, bout, bseg) = bbone
        fp.write(
"    bbone_in %d ; \n" % (bin) +
"    bbone_out %d ; \n" % (bout) +
"    bbone_segments %d ; \n" % (bseg))

    if flags & F_NOROT:
        fp.write("    use_inherit_rotation False ; \n")
    if flags & F_SCALE:
        fp.write("    use_inherit_scale True ; \n")
    else:
        fp.write("    use_inherit_scale False ; \n")
    fp.write("    layers Array ")

    bit = 1
    for n in range(32):
        if layers & bit:
            fp.write("1 ")
        else:
            fp.write("0 ")
        bit = bit << 1

#"    use_cyclic_offset %s ; \n" % cyc +
    fp.write(" ; \n" +
"    use_local_location %s ; \n" % lloc +
"    lock %s ; \n" % lock +
"    use_envelope_multiply False ; \n"+
"    hide_select %s ; \n" % (restr) +
"  end Bone \n")

def addBone24(bone, cond, roll, parent, flags, layers, bbone, fp):
    flags24 = 0
    if flags & F_CON:
        flags24 += 0x001
    if flags & F_DEF == 0:
        flags24 += 0x004
    if flags & F_NOSCALE:
        flags24 += 0x0e0

    fp.write("\n\tbone %s %s %x %x\n" % (bone, parent, flags24, layers))
    (x, y, z) = info.rigHeads[bone]
    fp.write("    head  %.6g %.6g %.6g  ;\n" % (x,y,z))
    (x, y, z) = info.rigTails[bone]
    fp.write("    tail %.6g %.6g %.6g  ;\n" % (x,y,z))
    fp.write("    roll %.6g %.6g ; \n" % (roll, roll))
    fp.write("\tend bone\n")
    return


def writeBoneGroups(fp, info):
    log.message("BG %s", info.config.boneGroups)
    if not fp:
        return
    for (name, color) in info.config.boneGroups:
        fp.write(
"    BoneGroup %s\n" % name +
"      name '%s' ;\n" % name +
"      color_set '%s' ;\n" % color +
"    end BoneGroup\n")
    return


def writeAction(fp, cond, name, action, lr, ikfk):
    fp.write("Action %s %s\n" % (name,cond))
    if ikfk:
        iklist = ["IK", "FK"]
    else:
        iklist = [""]
    if lr:
        for (bone, quats) in action:
            rquats = []
            for (t,x,y,z,w) in rquats:
                rquats.append((t,x,y,-z,-w))
            for ik in iklist:
                writeFCurves(fp, "%s%s_L" % (bone, ik), quats)
                writeFCurves(fp, "%s%s_R" % (bone, ik), rquats)
    else:
        for (bone, quats) in action:
            for ik in iklist:
                writeFCurves(fp, "%s%s" % (bone, ik), quats)
    fp.write("end Action\n\n")
    return


def writeFCurves(fp, name, quats):
    n = len(quats)
    for index in range(4):
        fp.write("\n" +
"  FCurve pose.bones[\"%s\"].rotation_quaternion %d\n" % (name, index))
        for m in range(n):
            t = quats[m][0]
            x = quats[m][index+1]
            fp.write("    kp %d %.4g ;\n" % (t,x))
        fp.write(
"    extrapolation 'CONSTANT' ;\n" +
"  end FCurve \n")
    return


def writeFkIkSwitch(fp, drivers):
    for (bone, cond, cnsFK, cnsIK, targ, channel, mx) in drivers:
        cnsData = ("ik", 'TRANSFORMS', [('OBJECT', info.name, targ, channel, C_LOC)])
        for cnsName in cnsFK:
            writeDriver(fp, cond, 'AVERAGE', "", "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, cnsName), -1, (mx,-mx), [cnsData])
        for cnsName in cnsIK:
            writeDriver(fp, cond, 'AVERAGE', "", "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, cnsName), -1, (0,mx), [cnsData])


def setupCircle(fp, name, r):
    fp.write("\n"+
"Mesh %s %s \n" % (name, name) +
"  Verts\n")
    for n in range(16):
        v = n*pi/8
        y = 0.5 + 0.02*sin(4*v)
        fp.write("    v %.3f %.3f %.3f ;\n" % (r*math.cos(v), y, r*math.sin(v)))
    fp.write(
"  end Verts\n" +
"  Edges\n")
    for n in range(15):
        fp.write("    e %d %d ;\n" % (n, n+1))
    fp.write("    e 15 0 ;\n")
    fp.write(
"  end Edges\n"+
"end Mesh\n"+
"Object %s MESH %s\n" % (name, name) +
"  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;\n"+
"  parent Refer Object CustomShapes ;\n"+
"end Object\n")
    return

def setupCubeMesh(fp, name, r, offs):
    try:
        (rx,ry,rz) = r
    except:
        (rx,ry,rz) = (r,r,r)
    try:
        (dx,dy,dz) = offs
    except:
        (dx,dy,dz) = (0,offs,0)

    fp.write("\n"+
"Mesh %s %s \n" % (name, name) +
"  Verts\n")
    for x in [-rx,rx]:
        for y in [-ry,ry]:
            for z in [-rz,rz]:
                fp.write("    v %.2f %.2f %.2f ;\n" % (x+dx,y+dy,z+dz))
    fp.write(
"  end Verts\n" +
"  Faces\n" +
"    f 0 1 3 2 ;\n" +
"    f 4 6 7 5 ;\n" +
"    f 0 2 6 4 ;\n" +
"    f 1 5 7 3 ;\n" +
"    f 1 0 4 5 ;\n" +
"    f 2 3 7 6 ;\n" +
"  end Faces\n" +
"end Mesh\n")
    return


def setupCube(fp, name, r, offs):
    setupCubeMesh(fp, name, r, offs)
    fp.write(
"Object %s MESH %s\n" % (name, name) +
"  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;\n" +
"  parent Refer Object CustomShapes ;\n" +
"end Object\n")


def setupCylinder(fp, name, r, h, offs, mat):
    try:
        (rx,ry) = r
    except:
        (rx,ry) = (r,r)
    try:
        (dx,dy,dz) = offs
    except:
        (dx,dy,dz) = (0,offs,0)

    fp.write(
"Mesh %s %s \n" % (name, name) +
"  Verts\n")
    z = h + dz
    for n in range(6):
        a = n*pi/3
        x = -rx*cos(a) + dx
        y = ry*sin(a) + dy
        fp.write("    v %.3f %.3f %.3f ;\n" % (x,z,y))
    z = dz
    for n in range(6):
        a = n*pi/3
        x = -rx*cos(a) + dx
        y = ry*sin(a) + dy
        fp.write("    v %.3f %.3f %.3f ;\n" % (x,z,y))
    fp.write(
"  end Verts\n" +
"  Edges\n" +
"    e 5 7 ;\n" +
"    e 0 1 ;\n" +
"    e 6 7 ;\n" +
"    e 3 7 ;\n" +
"    e 0 2 ;\n" +
"    e 1 3 ;\n" +
"    e 4 5 ;\n" +
"    e 1 5 ;\n" +
"    e 4 6 ;\n" +
"    e 2 3 ;\n" +
"    e 2 6 ;\n" +
"    e 0 4 ;\n" +
"  end Edges\n" +
"  Material %s ;\n" % mat +
"end Mesh\n" +
"Object %s MESH %s\n" % (name, name) +
"  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;\n" +
"  parent Refer Object CustomShapes ;\n" +
#"  Modifier Subsurf SUBSURF\n" +
#"  end Modifier\n" +
"end Object\n")


def setupCircles(fp):
    setupCircle(fp, "MHCircle01", 0.1)
    setupCircle(fp, "MHCircle025", 0.25)
    setupCircle(fp, "MHCircle05", 0.5)
    setupCircle(fp, "MHCircle10", 1.0)
    setupCircle(fp, "MHCircle15", 1.5)
    setupCircle(fp, "MHCircle20", 2.0)
    setupCube(fp, "MHCube01", 0.1, 0)
    setupCube(fp, "MHCube025", 0.25, 0)
    setupCube(fp, "MHCube05", 0.5, 0)
    setupCube(fp, "MHEndCube01", 0.1, 1)
    setupCube(fp, "MHChest", (0.7,0.25,0.5), (0,0.5,0.35))
    setupCube(fp, "MHRoot", (1.25,0.5,1.0), 1)
    return


def setupRig(info):
    info.rigHeads = {}
    info.rigTails = {}
    config = info.config
    config.vertexWeights = []
    config.customShapes = {}
    config.poseInfo = {}

    log.message("setupRig %s", config.rigtype)
    if config.rigtype == 'mhx':
        config.boneGroups = [
            ('Master', 'THEME13'),
            ('Spine', 'THEME05'),
            ('FK_L', 'THEME09'),
            ('FK_R', 'THEME02'),
            ('IK_L', 'THEME03'),
            ('IK_R', 'THEME04'),
        ]
        config.recalcRoll = "['Foot_L','Toe_L','Foot_R','Toe_R','DfmFoot_L','DfmToe_L','DfmFoot_R','DfmToe_R']"
        #config.recalcRoll = []
        config.gizmoFiles = ["./shared/mhx/templates/custom-shapes25.mhx", 
                      "./shared/mhx/templates/panel_gizmo25.mhx",
                      "./shared/mhx/templates/gizmos25.mhx"]

        config.objectProps = [("MhxRig", '"MHX"')]
        config.armatureProps = []
        config.headName = 'Head'
        config.preservevolume = False
        
        config.vertexGroupFiles = ["head", "bones", "palm", "tight"]
        if config.skirtrig == "own":
            config.vertexGroupFiles.append("skirt-rigged")    
        elif config.skirtrig == "inh":
            config.vertexGroupFiles.append("skirt")    

        if config.malerig:
            config.vertexGroupFiles.append( "male" )
                                                        
        joints = (
            rig_joints_25.DeformJoints +
            rig_body_25.BodyJoints +
            rig_body_25.FloorJoints +
            rig_arm_25.ArmJoints +
            rig_shoulder_25.ShoulderJoints +
            rig_finger_25.FingerJoints +
            rig_leg_25.LegJoints +
            #rig_toe_25.ToeJoints +
            rig_face_25.FaceJoints
        )            
        
        headsTails = (
            rig_body_25.BodyHeadsTails +
            rig_shoulder_25.ShoulderHeadsTails +
            rig_arm_25.ArmHeadsTails +
            rig_finger_25.FingerHeadsTails +
            rig_leg_25.LegHeadsTails +
            #rig_toe_25.ToeHeadsTails +
            rig_face_25.FaceHeadsTails
        )

        config.armatureBones = list(rig_body_25.BodyArmature1)
        if config.advancedspine:
            config.armatureBones += rig_body_25.BodyArmature2Advanced
        else:
            config.armatureBones += rig_body_25.BodyArmature2Simple
        config.armatureBones += rig_body_25.BodyArmature3
        if config.advancedspine:
            config.armatureBones += rig_body_25.BodyArmature4Advanced
        else:
            config.armatureBones += rig_body_25.BodyArmature4Simple
        config.armatureBones += rig_body_25.BodyArmature5

        config.armatureBones += (
            rig_shoulder_25.ShoulderArmature1 +
            rig_shoulder_25.ShoulderArmature2 +
            rig_arm_25.ArmArmature +            
            rig_finger_25.FingerArmature +
            rig_leg_25.LegArmature +
            #rig_toe_25.ToeArmature +
            rig_face_25.FaceArmature
        )

    elif config.rigtype == "rigify":
        config.boneGroups = []
        config.recalcRoll = []              
        config.vertexGroupFiles = ["head", "rigify"]
        config.gizmoFiles = ["./shared/mhx/templates/panel_gizmo25.mhx",
                          "./shared/mhx/templates/rigify_gizmo25.mhx"]
        config.headName = 'head'
        config.preservevolume = True
        faceArmature = swapParentNames(rig_face_25.FaceArmature, 
                           {'Head' : 'head', 'MasterFloor' : None} )
            
        joints = (
            rig_joints_25.DeformJoints +
            rig_body_25.BodyJoints +
            rig_body_25.FloorJoints +
            rigify_rig.RigifyJoints +
            rig_face_25.FaceJoints
        )
        
        headsTails = (
            rigify_rig.RigifyHeadsTails +
            rig_face_25.FaceHeadsTails
        )

        config.armatureBones = (
            rigify_rig.RigifyArmature +
            faceArmature
        )

        config.objectProps = rigify_rig.RigifyObjectProps + [("MhxRig", '"Rigify"')]
        config.armatureProps = rigify_rig.RigifyArmatureProps

    else:
        rigfile = "data/rigs/%s.rig" % config.rigtype
        (locations, boneList, config.vertexWeights) = read_rig.readRigFile(rigfile, info.mesh)        
        joints = (
            rig_joints_25.DeformJoints +
            rig_body_25.FloorJoints +
            rig_face_25.FaceJoints
        )
        headsTails = []
        config.armatureBones = []
        #if config.facepanel:            
        #    joints += rig_panel_25.PanelJoints
        #    headsTails += rig_panel_25.PanelHeadsTails
        #    config.armatureBones += rig_panel_25.PanelArmature
        newSetupJoints(info, joints)        
        moveOriginToFloor(info)
        for (bone, head, tail) in headsTails:
            info.rigHeads[bone] = findLocation(info, head)
            info.rigTails[bone] = findLocation(info, tail)

        appendRigBones(boneList, info.mesh, "", L_MAIN, [], info)
        log.debug("BL %s", str(boneList[0]))
        config.boneGroups = []
        config.recalcRoll = []              
        config.vertexGroupFiles = []
        config.gizmoFiles = []
        config.headName = 'Head'
        config.objectProps = [("MhxRig", '"%s"' % config.rigtype)]
        config.armatureProps = []
        config.customProps = []
        log.message("Default rig %s", config.rigtype)
        return

    """        
    if config.facepanel:            
        joints += rig_panel_25.PanelJoints
        headsTails += rig_panel_25.PanelHeadsTails
        config.armatureBones += rig_panel_25.PanelArmature
    """
    
    if config.rigtype == 'mhx':
        if config.skirtrig == "own":
            joints += rig_skirt_25.SkirtJoints
            headsTails += rig_skirt_25.SkirtHeadsTails
            config.armatureBones += rig_skirt_25.SkirtArmature        
        if config.malerig:
            config.armatureBones += rig_body_25.MaleArmature        

    (custJoints, custHeadsTails, custArmature, config.customProps) = mhx_custom.setupCustomRig(config)
    joints += custJoints
    headsTails += custHeadsTails
    config.armatureBones += custArmature
    
    newSetupJoints(info, joints)
    moveOriginToFloor(info)    

    if config.rigtype == 'mhx':
        rig_body_25.BodyDynamicLocations()
    for (bone, head, tail) in headsTails:
        info.rigHeads[bone] = findLocation(info, head)
        info.rigTails[bone] = findLocation(info, tail)
        
    #print "H1", info.rigHeads["UpLeg_L"]
    #print "T1", info.rigTails["UpLeg_L"]

    if not config.clothesrig:
        return
    body = info.rigHeads.keys()
    for proxy in info.proxies.values():
        if proxy.rig:
            verts = []
            for bary in proxy.realVerts:
                verts.append(mh2proxy.proxyCoord(bary))
            (locations, boneList, weights) = read_rig.readRigFile(proxy.rig, info.mesh, verts=verts) 
            proxy.weights = prefixWeights(weights, proxy.name, body)
            appendRigBones(boneList, info.mesh, proxy.name, L_CLO, body, info)
    return


def prefixWeights(weights, prefix, body):
    pweights = {}
    for name in weights.keys():
        if name in body:
            pweights[name] = weights[name]
        else:
            pweights[prefix+name] = weights[name]
    return pweights


def appendRigBones(boneList, obj, prefix, layer, body, info):        
    config = info.config
    for data in boneList:
        (bone0, head, tail, roll, parent0, options) = data
        if bone0 in body:
            continue
        bone = prefix + bone0
        if parent0 == "-":
            parent = None
        elif parent0 in body:
            parent = parent0
        else:
            parent = prefix + parent0
        flags = F_DEF|F_CON
        for (key, value) in options.items():
            if key == "-nc":
                flags &= ~F_CON
            elif key == "-nd":
                flags &= ~F_DEF
            elif key == "-res":
                flags |= F_RES
            elif key == "-circ":
                name = "Circ"+value[0]
                config.customShapes[name] = (key, int(value[0]))
                addPoseInfo(bone, ("CS", name), config)
                flags |= F_WIR
            elif key == "-box":
                name = "Box" + value[0]
                config.customShapes[name] = (key, int(value[0]))
                addPoseInfo(bone, ("CS", name), config)
                flags |= F_WIR
            elif key == "-ik":
                try:
                    pt = options["-pt"]
                except KeyError:
                    pt = None
                log.debug("%s %s", value, pt)
                value.append(pt)
                addPoseInfo(bone, ("IK", value), config)
            elif key == "-ik":
                pass
        config.armatureBones.append((bone, roll, parent, flags, layer, NoBB))
        info.rigHeads[bone] = aljabr.vsub(head, info.origin)
        info.rigTails[bone] = aljabr.vsub(tail, info.origin)
        
        
def addPoseInfo(bone, info, config):
    try:
        config.poseInfo[bone]
    except:
        config.poseInfo[bone] = []
    config.poseInfo[bone].append(info)
    return        
        

def swapParentNames(bones, changes):
    nbones = []
    for bone in bones:
        (name, roll, par, flags, level, bb) = bone
        try:
            nbones.append( (name, roll, changes[par], flags, level, bb) )
        except KeyError:
            nbones.append(bone)
    return nbones


def writeControlPoses(fp, info):
    config = info.config
    writeBoneGroups(fp, info)
    if info.config.rigtype == 'mhx':            
        rig_body_25.BodyControlPoses(fp, info)
        rig_shoulder_25.ShoulderControlPoses(fp, info)
        rig_arm_25.ArmControlPoses(fp, info)
        rig_finger_25.FingerControlPoses(fp, info)
        rig_leg_25.LegControlPoses(fp, info)
        #rig_toe_25.ToeControlPoses(fp, info)
        rig_face_25.FaceControlPoses(fp, info)
        if config.malerig:
            rig_body_25.MaleControlPoses(fp, info)
        if config.skirtrig == "own":
            rig_skirt_25.SkirtControlPoses(fp, info)
    elif config.rigtype == 'blenrig':
        blenrig_rig.BlenrigWritePoses(fp, info)
    elif config.rigtype == 'rigify':
        rigify_rig.RigifyWritePoses(fp, info)
        rig_face_25.FaceControlPoses(fp, info)
        
    #if config.facepanel:
    #    rig_panel_25.PanelControlPoses(fp, info)
        
    for (bone, cinfo) in info.config.poseInfo.items():
        cs = None
        constraints = []
        for (key, value) in cinfo:
            if key == "CS":
                cs = value
            elif key == "IK":
                goal = value[0]
                n = int(value[1])
                inf = float(value[2])
                pt = value[3]
                if pt:
                    log.debug("%s %s %s %s", goal, n, inf, pt)
                    subtar = pt[0]
                    poleAngle = float(pt[1])
                    pt = (poleAngle, subtar)
                constraints =  [('IK', 0, inf, ['IK', goal, n, pt, (True,False,True)])]
        posebone.addPoseBone(fp, info, bone, cs, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, constraints)       
        
    #for (path, modname) in config.customRigs:
    #    mod = sys.modules[modname]                
    #    mod.ControlPoses(fp, config)

    return


def writeAllActions(fp, info):
    #rig_arm_25.ArmWriteActions(fp)
    #rig_leg_25.LegWriteActions(fp)
    #rig_finger_25.FingerWriteActions(fp)
    return


def writeAllDrivers(fp, info):
    config = info.config
    if config.rigtype == 'mhx':      
        driverList = (
            armature.drivers.writePropDrivers(fp, info, rig_arm_25.ArmPropDrivers, "", "Mha") +
            armature.drivers.writePropDrivers(fp, info, rig_arm_25.ArmPropLRDrivers, "_L", "Mha") +
            armature.drivers.writePropDrivers(fp, info, rig_arm_25.ArmPropLRDrivers, "_R", "Mha") +
            armature.drivers.writePropDrivers(fp, info, rig_arm_25.SoftArmPropLRDrivers, "_L", "Mha") +
            armature.drivers.writePropDrivers(fp, info, rig_arm_25.SoftArmPropLRDrivers, "_R", "Mha") +
            #writeScriptedBoneDrivers(fp, rig_leg_25.LegBoneDrivers) +
            armature.drivers.writePropDrivers(fp, info, rig_leg_25.LegPropDrivers, "", "Mha") +
            armature.drivers.writePropDrivers(fp, info, rig_leg_25.LegPropLRDrivers, "_L", "Mha") +
            armature.drivers.writePropDrivers(fp, info, rig_leg_25.LegPropLRDrivers, "_R", "Mha") +
            armature.drivers.writePropDrivers(fp, info, rig_leg_25.SoftLegPropLRDrivers, "_L", "Mha") +
            armature.drivers.writePropDrivers(fp, info, rig_leg_25.SoftLegPropLRDrivers, "_R", "Mha") +
            armature.drivers.writePropDrivers(fp, info, rig_body_25.BodyPropDrivers, "", "Mha")
        )
        if config.advancedspine:
            driverList += armature.drivers.writePropDrivers(fp, info, rig_body_25.BodyPropDriversAdvanced, "", "Mha") 
        driverList += (
            armature.drivers.writePropDrivers(fp, info, rig_face_25.FacePropDrivers, "", "Mha") +
            armature.drivers.writePropDrivers(fp, info, rig_face_25.SoftFacePropDrivers, "", "Mha")
        )
        fingDrivers = rig_finger_25.getFingerPropDrivers()
        driverList += (
            armature.drivers.writePropDrivers(fp, info, fingDrivers, "_L", "Mha") +
            armature.drivers.writePropDrivers(fp, info, fingDrivers, "_R", "Mha") +
            #rig_panel_25.FingerControlDrivers(fp)
            armature.drivers.writeMuscleDrivers(fp, rig_shoulder_25.ShoulderDeformDrivers, info.name) +
            armature.drivers.writeMuscleDrivers(fp, rig_arm_25.ArmDeformDrivers, info.name) +
            armature.drivers.writeMuscleDrivers(fp, rig_leg_25.LegDeformDrivers, info.name)
        )
        faceDrivers = rig_face_25.FaceDeformDrivers(fp, info)
        driverList += armature.drivers.writeDrivers(fp, True, faceDrivers)
        return driverList
    elif config.rigtype == 'blenrig':            
        drivers = blenrig_rig.getBlenrigDrivers()
        armature.drivers.writeDrivers(fp, True, drivers)
    elif rigtype == 'rigify':            
        rig_face_25.FaceDeformDrivers(fp, info)        
        armature.drivers.writePropDrivers(fp, info, rig_face_25.FacePropDrivers, "", "Mha")
        armature.drivers.writePropDrivers(fp, info, rig_face_25.SoftFacePropDrivers, "", "Mha")
    return []
    

def writeAllProperties(fp, typ, info):
    config = info.config
    if typ != 'Object':
        return
    for (key, val) in config.objectProps:
        fp.write("  Property %s %s ;\n" % (key, val))
    for (key, val, string, min, max) in config.customProps:
        fp.write('  DefProp Float Mha%s %.2f %s min=-%.2f,max=%.2f ;\n' % (key, val, string, min, max) )

    """
    if (config.faceshapes and not config.facepanel):
        fp.write("#if toggle&T_Shapekeys\n")
        for skey in rig_panel_25.BodyLanguageShapeDrivers.keys():
            fp.write("  DefProp Float Mhf%s 0.0 %s min=-1.0,max=2.0 ;\n" % (skey, skey))
        fp.write("#endif\n")
    """
    
    if config.expressionunits:
        fp.write("#if toggle&T_Shapekeys\n")
        for skey in read_shapekeys.ExpressionUnits:
            fp.write("  DefProp Float Mhs%s 0.0 %s min=-1.0,max=2.0 ;\n" % (skey, skey))
        fp.write("#endif\n")
    return


