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

Parser for armature
"""

import os
import math
import gui3d
import log
from collections import OrderedDict
import io_json

import numpy as np
import numpy.linalg as la
import transformations as tm

from .flags import *
from .utils import *
from .armature import Bone

from . import rig_joints
from . import rig_bones
from . import rig_muscle
from . import rig_face
from . import rig_control
from . import rig_merge

#-------------------------------------------------------------------------------
#   Parser base class.
#-------------------------------------------------------------------------------

class Parser:

    def __init__(self, amt, human):
        self.armature = amt
        self.human = human
        options = amt.options

        self.locations = {}
        self.origin = [0,0,0]
        self.normals = {}
        self.headsTails = None
        self.parents = {}
        self.ikChains = {}
        self.loadedShapes = {}
        self.customShapes = {}
        self.gizmos = {}
        self.constraints = {}
        self.rotationLimits = {}
        self.drivers = []
        self.lrDrivers = []

        self.vertexGroupFiles = []

        self.master = None
        self.headName = 'head'
        self.root = "hips"

        if options.useMuscles:
            self.vertexGroupFiles = ["head", "muscles", "hand"]
        else:
            self.vertexGroupFiles = ["head", "bones", "hand"]

        self.joints = (
            rig_joints.Joints +
            rig_bones.Joints +
            rig_face.Joints +
            rig_control.Joints
        )

        self.planes = rig_bones.Planes
        self.planeJoints = rig_control.PlaneJoints

        self.headsTails = mergeDicts([
            rig_bones.HeadsTails,
            rig_face.HeadsTails,
            rig_control.HeadsTails,
        ])

        self.constraints = mergeDicts([
            rig_bones.Constraints,
            rig_face.Constraints
        ])

        self.rotationLimits = mergeDicts([
            rig_bones.RotationLimits,
            rig_face.RotationLimits
        ])

        self.customShapes = mergeDicts([
            rig_bones.CustomShapes,
            rig_face.CustomShapes
        ])

        if options.useMuscles:
            self.joints += rig_muscle.Joints
            addDict(rig_muscle.HeadsTails, self.headsTails)
            addDict(rig_muscle.Constraints, self.constraints)
            addDict(rig_muscle.CustomShapes, self.customShapes)
            addDict(rig_muscle.RotationLimits, self.rotationLimits)

        if options.useFingers:
            addDict(rig_control.FingerConstraints, self.constraints)
            self.lrDrivers += rig_control.FingerPropLRDrivers

        self.splitBones = {}
        if options.useSplitBones:
            self.splitBones = {
                "forearm" :     (3, "hand", False),
            }

        self.objectProps = rig_bones.ObjectProps
        self.armatureProps = rig_bones.ArmatureProps


    def createBones(self, boneInfo):
        amt = self.armature
        options = amt.options

        if amt.done:
            halt
        amt.done = True

        self.addBones(rig_bones.Armature, boneInfo)
        self.addBones(rig_face.Armature, boneInfo)

        if options.useDeformBones:
            self.addDeformBones(rig_bones.Armature, boneInfo)
            self.addDeformBones(rig_face.Armature, boneInfo)

        if options.useMasterBone:
            self.master = 'master'
            self.addBones(rig_control.MasterArmature, boneInfo)

        if options.useMuscles:
            self.addBones(rig_muscle.Armature, boneInfo)

        if options.useIkLegs:
            self.addBones(rig_control.IkLegArmature, boneInfo)
            addDict(rig_control.IkLegConstraints, self.constraints)
            addDict(rig_control.IkLegChains, self.ikChains)
            addDict(rig_control.IkLegParents, self.parents)
            self.lrDrivers += rig_control.IkLegPropLRDrivers

        if options.useIkArms:
            self.addBones(rig_control.IkArmArmature, boneInfo)
            addDict(rig_control.IkArmConstraints, self.constraints)
            addDict(rig_control.IkArmChains, self.ikChains)
            addDict(rig_control.IkArmParents, self.parents)
            self.lrDrivers += rig_control.IkArmPropLRDrivers

        if options.useIkLegs or options.useIkArms:
            self.addIkChains(rig_bones.Armature, boneInfo, self.ikChains)

        if options.useFingers:
            self.addBones(rig_control.FingerArmature, boneInfo)

        if options.useCorrectives:
            self.addCSysBones(rig_control.CoordinateSystems, boneInfo)

        if options.addConnectingBones:
            extras = []
            for bone in boneInfo.values():
                if bone.parent:
                    head,_ = self.getHeadTail(bone.name)
                    _,ptail = self.getHeadTail(bone.parent)
                    if head != ptail:
                        connector = Bone(amt, "_"+bone.name)
                        connector.parent = bone.parent
                        bone.parent = connector
                        extras.append(connector)
                        self.setHeadTail(connector, ptail, head)

            for bone in extras:
                boneInfo[bone.name] = bone

        if options.useCustomShapes:
            struct = io_json.loadJson("shared/armature/gizmos.json")
            for name,gizmo in self.customShapes.items():
                if gizmo:
                    self.gizmos[gizmo] = struct[gizmo]

        """
        if options.skirtRig == "own":
            self.joints += rig_skirt.Joints
            self.headsTails += rig_skirt.HeadsTails
            self.boneDefs += rig_skirt.Armature

        if options.maleRig:
            self.boneDefs += rig_body.MaleArmature

        if options.facepanel:
            self.joints += rig_panel.Joints
            self.headsTails += rig_panel.HeadsTails
            self.boneDefs += rig_panel.Armature

        if False and options.custom:
            (custJoints, custHeadsTails, custArmature, self.customProps) = exportutils.custom.setupCustomRig(options)
            self.joints += custJoints
            self.headsTails += custHeadsTails
            self.boneDefs += custArmature
        """

        self.getVertexGroups(boneInfo)

        if options.mergeSpine:
            self.mergeBones(rig_merge.SpineMergers, boneInfo)

        if options.mergeFingers:
            self.mergeBones(rig_merge.FingerMergers, boneInfo)

        if options.mergePalms:
            self.mergeBones(rig_merge.PalmMergers, boneInfo)

        if options.mergeHead:
            self.mergeBones(rig_merge.HeadMergers, boneInfo)

        for bone in boneInfo.values():
            if bone.parent:
                parent = boneInfo[bone.parent]
                parent.children.append(bone)
            elif self.master:
                if bone.name == self.master:
                    amt.roots.append(bone)
                else:
                    bone.parent = self.master
                    master = boneInfo[self.master]
                    master.children.append(bone)
            else:
                amt.roots.append(bone)

        for root in amt.roots:
            self.sortBones(root, amt.hierarchy)

        for bname,data in self.customShapes.items():
            amt.bones[bname].customShape = data

        for bname,data in self.constraints.items():
            try:
                amt.bones[bname].constraints = data
            except KeyError:
                log.message("Warning: constraint for undefined bone %s" % bname)


    def setup(self):
        amt = self.armature
        options = amt.options

        self.setupJoints(self.human)
        self.setupNormals()
        self.setupPlaneJoints()
        self.moveOriginToFloor(options.feetOnGround)
        self.createBones({})

        for bone in amt.bones.values():
            head,tail = self.headsTails[bone.name]
            bone.setBone(self.findLocation(head), self.findLocation(tail))

        for bone in amt.bones.values():
            if isinstance(bone.roll, str):
                bone.roll = amt.bones[bone.roll].roll
            elif isinstance(bone.roll, Bone):
                bone.roll = bone.roll.roll
            elif isinstance(bone.roll, tuple):
                bname,angle = bone.roll
                bone.roll = amt.bones[bname].roll + angle
        self.postSetup()


    def postSetup(self):
        return


    def setupNormals(self):
        for plane,joints in self.planes.items():
            j1,j2,j3 = joints
            p1 = self.locations[j1]
            p2 = self.locations[j2]
            p3 = self.locations[j3]
            pvec = getUnitVector(p2-p1)
            yvec = getUnitVector(p3-p2)
            if pvec is None or yvec is None:
                self.normals[plane] = None
            else:
                self.normals[plane] = getUnitVector(np.cross(yvec, pvec))


    def setupJoints (self, human):
        """
        Evaluate symbolic expressions for joint locations and store them in self.locations.
        Joint locations are specified symbolically in the *Joints list in the beginning of the
        rig_*.py files (e.g. ArmJoints in rig_arm.py).
        """

        obj = human.meshData
        for (key, typ, data) in self.joints:
            if typ == 'j':
                loc = calcJointPos(obj, data)
                self.locations[key] = loc
                self.locations[data] = loc
            elif typ == 'v':
                v = int(data)
                self.locations[key] = obj.coord[v]
            elif typ == 'x':
                self.locations[key] = np.array((float(data[0]), float(data[2]), -float(data[1])))
            elif typ == 'vo':
                v = int(data[0])
                offset = np.array((float(data[1]), float(data[3]), -float(data[2])))
                self.locations[key] = (obj.coord[v] + offset)
            elif typ == 'vl':
                ((k1, v1), (k2, v2)) = data
                loc1 = obj.coord[int(v1)]
                loc2 = obj.coord[int(v2)]
                self.locations[key] = (k1*loc1 + k2*loc2)
            elif typ == 'f':
                (raw, head, tail, offs) = data
                rloc = self.locations[raw]
                hloc = self.locations[head]
                tloc = self.locations[tail]
                vec = tloc - hloc
                vraw = rloc - hloc
                x = np.dot(vec, vraw)/np.dot(vec,vec)
                self.locations[key] = hloc + x*vec + np.array(offs)
            elif typ == 'b':
                self.locations[key] = self.locations[data]
            elif typ == 'p':
                x = self.locations[data[0]]
                y = self.locations[data[1]]
                z = self.locations[data[2]]
                self.locations[key] = np.array((x[0],y[1],z[2]))
            elif typ == 'vz':
                v = int(data[0])
                z = obj.coord[v][2]
                loc = self.locations[data[1]]
                self.locations[key] = np.array((loc[0],loc[1],z))
            elif typ == 'X':
                r = self.locations[data[0]]
                (x,y,z) = data[1]
                r1 = np.array([float(x), float(y), float(z)])
                self.locations[key] = np.cross(r, r1)
            elif typ == 'l':
                ((k1, joint1), (k2, joint2)) = data
                self.locations[key] = k1*self.locations[joint1] + k2*self.locations[joint2]
            elif typ == 'o':
                (joint, offsSym) = data
                if type(offsSym) == str:
                    offs = self.locations[offsSym]
                else:
                    offs = np.array(offsSym)
                self.locations[key] = self.locations[joint] + offs
            else:
                raise NameError("Unknown %s" % typ)
        return


    def setupPlaneJoints (self):
        for key,data in self.planeJoints:
            p0,plane,dist = data
            x0 = self.locations[p0]
            p1,p2,p3 = self.planes[plane]
            vec = self.locations[p3] - self.locations[p1]
            vec /= math.sqrt(np.dot(vec,vec))
            n = self.normals[plane]
            t = np.cross(n, vec)
            self.locations[key] = x0 + dist*t


    def moveOriginToFloor(self, feetOnGround):
        if feetOnGround:
            self.origin = self.locations['ground']
            for key in self.locations.keys():
                self.locations[key] = self.locations[key] - self.origin
        else:
            self.origin = np.array([0,0,0], float)
        return


    def findLocation(self, joint):
        if isinstance(joint, str):
            return self.locations[joint]
        else:
            (first, second) = joint
            if isinstance(first, str):
                return self.locations[first] + second
            else:
                w1,j1 = first
                w2,j2 = second
                return w1*self.locations[j1] + w2*self.locations[j2]


    def distance(self, joint1, joint2):
        vec = self.locations[joint2] - self.locations[joint1]
        return math.sqrt(np.dot(vec,vec))


    def getHeadTail(self, bone):
        return self.headsTails[bone]


    def setHeadTail(self, bone, head, tail):
        self.headsTails[bone] = (head,tail)


    def prefixWeights(self, weights, prefix):
        pweights = {}
        for name in weights.keys():
            if name in self.heads:
                pweights[name] = weights[name]
            else:
                pweights[prefix+name] = weights[name]
        return pweights


    def sortBones(self, bone, hier):
        self.armature.bones[bone.name] = bone
        subhier = []
        hier.append([bone, subhier])
        for child in bone.children:
            self.sortBones(child, subhier)


    def addBones(self, dict, boneInfo):
        for bname,info in dict.items():
            bone = boneInfo[bname] = Bone(self.armature, bname)
            bone.fromInfo(info)


    def getParent(self, bone):
        return bone.parent


    def addIkChains(self, generic, boneInfo, ikChains):
        """
        Adds FK and IK versions of the bones in the chain, and add CopyTransform
        constraints to the original bone, which is moved to the L_HELP layer. E.g.
        shin.L => shin.fk.L, shin.ik.L, shin.L
        """

        amt = self.armature
        options = amt.options

        for bname in generic.keys():
            bone = boneInfo[bname]
            headTail = self.headsTails[bname]
            base,ext = splitBoneName(bname)
            bone.parent = self.getParent(bone)

            if base in ikChains.keys():
                pbase,pext = splitBoneName(bone.parent)
                value = ikChains[base]
                type = value[0]
                if type == "DownStream":
                    _,layer,cnsname = value
                    fkParent = getFkName(pbase,pext)
                elif type == "Upstream":
                    _,layer,cnsname = value
                    fkParent = ikParent = bone.parent
                elif type == "Leaf":
                    _, layer, count, cnsname, target, pole, lang, rang = value
                    fkParent = getFkName(pbase,pext)
                    ikParent = getIkName(pbase,pext)
                else:
                    raise NameError("Unknown IKChain type %s" % type)

                if ext == ".R":
                    layer <<= 16

                fkName = getFkName(base,ext)
                self.headsTails[fkName] = headTail
                fkBone = boneInfo[fkName] = Bone(amt, fkName)
                fkBone.fromInfo((bname, fkParent, F_WIR, layer<<1))

                customShape = self.customShapes[bone.name]
                self.customShapes[fkName] = customShape
                self.customShapes[bone.name] = None
                bone.layers = L_HELP

                cns = copyTransform(fkName, cnsname+"FK")
                safeAppendToDict(self.constraints, bname, cns)

                if type == "DownStream":
                    continue

                ikName = base + ".ik" + ext
                self.headsTails[ikName] = headTail
                ikBone = boneInfo[ikName] = Bone(amt, ikName)
                ikBone.fromInfo((bname, ikParent, F_WIR, layer))

                self.customShapes[ikName] = customShape
                self.constraints[bname].append( copyTransform(ikName, cnsname+"IK", 0) )

                if type == "Leaf":
                    words = bone.parent.rsplit(".", 1)
                    pbase = words[0]
                    if len(words) == 1:
                        pext = ""
                    else:
                        pext = "." + words[1]
                    fkBone.parent = pbase + ".fk" + pext
                    ikBone.parent = pbase + ".ik" + pext

                    ikTarget = target + ".ik" + ext
                    poleTarget = pole + ".ik" + ext
                    if ext == ".L":
                        poleAngle = lang
                    else:
                        poleAngle = rang

                    cns = ('IK', 0, 1, ['IK', ikTarget, count, (poleAngle, poleTarget), (True, False,False)])
                    safeAppendToDict(self.constraints, ikName, cns)

            else:
                bone.deform = False


    def addDeformBones(self, generic, boneInfo):
        """
        Add deform bones with CopyTransform constraints to the original bone.
        Deform bones start with "DEF-", as in Rigify.
        Also split selected bones into two or three parts for better deformation,
        and constrain them to copy the partially.
        E.g. forearm.L => DEF-forearm.01.L, DEF-forearm.02.L, DEF-forearm.03.L
        """

        amt = self.armature
        options = amt.options

        if not (options.useDeformBones or options.useSplitBones):
            return

        for bname in generic.keys():
            bone = boneInfo[bname]
            if not bone.deform:
                continue
            headTail = self.headsTails[bname]
            base,ext = splitBoneName(bname)
            bone.deform = False
            bone.parent = self.getParent(bone)
            if bone.parent and options.useDeformBones:
                pbase, pext = splitBoneName(bone.parent)
                if pbase in self.splitBones.keys():
                    npieces = self.splitBones[pbase][0]
                    defParent = "DEF-" + pbase + ".0" + str(npieces) + pext
                else:
                    parbone = boneInfo[bone.parent]
                    if parbone.deform:
                        defParent = "DEF-" + bone.parent
                    else:
                        defParent = bone.parent
            else:
                defParent = bone.parent

            if options.useSplitBones and (base in self.splitBones.keys()):
                npieces,target,numAfter = self.splitBones[base]
                defName1,defName2,defName3 = splitBonesNames(base, ext, numAfter)
                head,tail = headTail
                fkName = base + ".fk" + ext
                ikName = base + ".ik" + ext
                self.constraints[defName1] = [
                    ('IK', 0, 1, ['IK', target+ext, 1, None, (True, False,True)])
                ]
                if npieces == 2:
                    self.headsTails[defName1] = (head, ((0.5,head),(0.5,tail)))
                    self.headsTails[defName2] = (((0.5,head),(0.5,tail)), tail)
                    defBone1 = boneInfo[defName1] = Bone(amt, defName1)
                    defBone1.fromInfo((bone, defParent, F_DEF+F_CON, L_DEF))
                    defBone2 = boneInfo[defName2] = Bone(amt, defName2)
                    defBone2.fromInfo((bone, bone.name, F_DEF, L_DEF))
                elif npieces == 3:
                    self.headsTails[defName1] = (head, ((0.667,head),(0.333,tail)))
                    self.headsTails[defName2] = (((0.667,head),(0.333,tail)), ((0.333,head),(0.667,tail)))
                    self.headsTails[defName3] = (((0.333,head),(0.667,tail)), tail)
                    defBone1 = boneInfo[defName1] = Bone(amt, defName1)
                    defBone1.fromInfo((bone, defParent, F_DEF+F_CON, L_DEF))
                    defBone3 = boneInfo[defName3] = Bone(amt, defName3)
                    defBone3.fromInfo((bone, bone.name, F_DEF, L_DEF))
                    defBone2 = boneInfo[defName2] = Bone(amt, defName2)
                    defBone2.fromInfo((bone, defParent, F_DEF, L_DEF))
                    self.constraints[defName2] = [
                        ('CopyLoc', 0, 1, ["CopyLoc", defName1, (1,1,1), (0,0,0), 1, False]),
                        ('CopyRot', 0, 1, [defName1, defName1, (1,1,1), (0,0,0), False]),
                        ('CopyRot', 0, 0.5, [bone.name, bone.name, (1,1,1), (0,0,0), False])
                    ]

            elif options.useDeformBones:
                defName = "DEF-"+bname
                self.headsTails[defName] = headTail
                defBone = boneInfo[defName] = Bone(amt, defName)
                defBone.fromInfo((bone, defParent, F_DEF, L_DEF))
                self.constraints[defName] = [copyTransform(bone.name, bone.name)]

        return boneInfo


    def getVertexGroups(self, boneInfo):
        """
        Read vertex groups from specified files, and do some manipulations.
        If the rig has deform bones, prefix vertex group names with "DEF-".
        If some bones are split, split the vertex groups into two or three.
        Rigify uses deform and split names but not bones, because the rigify
        script will fix that in Blender.
        """

        amt = self.armature
        options = amt.options

        self.vertexGroupFiles += ["leftright"]
        vgroupList = []
        vgroups = {}
        for file in self.vertexGroupFiles:
            filepath = os.path.join("shared/armature/vertexgroups", file+".vgrp")
            readVertexGroups(filepath, vgroups, vgroupList)

        if options.useDeformBones or options.useDeformNames:
            for bname,vgroup in vgroupList:
                base = splitBoneName(bname)[0]
                if base in self.splitBones.keys():
                    self.splitVertexGroup(bname, vgroup)
                elif not options.useSplitBones:
                    defName = "DEF-"+bname
                    amt.vertexWeights[defName] = vgroup
                else:
                    defName = "DEF-"+bname
                    try:
                        boneInfo[defName]
                        amt.vertexWeights[defName] = vgroup
                    except KeyError:
                        amt.vertexWeights[bname] = vgroup

        elif options.useSplitBones or options.useSplitNames:
            for bname,vgroup in vgroupList:
                base = splitBoneName(bname)[0]
                if base in self.splitBones.keys():
                    self.splitVertexGroup(bname, vgroup)
                else:
                    amt.vertexWeights[bname] = vgroup

        else:
            for bname,vgroup in vgroupList:
                amt.vertexWeights[bname] = vgroup


    def splitVertexGroup(self, bname, vgroup):
        """
        Splits a vertex group into two or three, with weights distributed
        linearly along the bone.
        """

        amt = self.armature
        base,ext = splitBoneName(bname)
        npieces,target,numAfter = self.splitBones[base]
        defName1,defName2,defName3 = splitBonesNames(base, ext, numAfter)

        head,tail = self.headsTails[bname]
        vec = getUnitVector(self.locations[head] - self.locations[tail])
        orig = self.locations[head] + self.origin

        vgroup1 = []
        vgroup2 = []
        vgroup3 = []
        obj = self.human.meshData
        if npieces == 2:
            for vn,w in vgroup:
                y = obj.coord[vn] - orig
                x = np.dot(vec,y)
                if x < 0:
                    vgroup1.append((vn,w))
                elif x < 0.5:
                    vgroup1.append((vn, (1-x)*w))
                    vgroup2.append((vn, x*w))
                else:
                    vgroup2.append((vn,w))
            amt.vertexWeights[defName1] = vgroup1
            amt.vertexWeights[defName2] = vgroup2
        elif npieces == 3:
            for vn,w in vgroup:
                y = obj.coord[vn] - orig
                x = np.dot(vec,y)
                if x < 0:
                    vgroup1.append((vn,w))
                elif x < 0.5:
                    vgroup1.append((vn, (1-2*x)*w))
                    vgroup2.append((vn, (2*x)*w))
                elif x < 1:
                    vgroup2.append((vn, (2-2*x)*w))
                    vgroup3.append((vn, (2*x-1)*w))
                else:
                    vgroup3.append((vn,w))
            amt.vertexWeights[defName1] = vgroup1
            amt.vertexWeights[defName2] = vgroup2
            amt.vertexWeights[defName3] = vgroup3


    def mergeBones(self, mergers, boneInfo):
        amt = self.armature
        for bname, merged in mergers.items():
            vgroup = amt.vertexWeights[bname]
            for mbone in merged:
                if mbone != bname:
                    vgroup += amt.vertexWeights[mbone]
                    del amt.vertexWeights[mbone]
                    del boneInfo[mbone]
                    for child in boneInfo.values():
                        if child.parent == mbone:
                            child.parent = bname
        amt.vertexWeights[bname] = mergeWeights(vgroup)


    def addCSysBones(self, csysList, boneInfo):
        """
        Add a local coordinate system consisting of six bones around the head
        of a given bone. Useful for setting up ROTATION_DIFF drivers for
        corrective shapekeys.
        Y axis: parallel to bone.
        X axis: main bend axis, normal to plane.
        Z axis: third axis.
        """

        for bname,ikTarget in csysList:
            bone = boneInfo[bname]
            parent = self.getParent(bone)
            head,_ = self.headsTails[bname]

            self.addCSysBone(bname, "_X1", boneInfo, parent, head, (1,0,0), 0)
            self.addCSysBone(bname, "_X2", boneInfo, parent, head, (-1,0,0), 0)
            csysY1 = self.addCSysBone(bname, "_Y1", boneInfo, parent, head, (0,1,0), 90*D)
            csysY2 = self.addCSysBone(bname, "_Y2", boneInfo, parent, head, (0,-1,0), -90*D)
            self.addCSysBone(bname, "_Z1", boneInfo, parent, head, (0,0,1), 0)
            self.addCSysBone(bname, "_Z2", boneInfo, parent, head, (0,0,-1), 0)

            self.constraints[csysY1] = [('IK', 0, 1, ['IK', ikTarget, 1, None, (True, False,False)])]
            self.constraints[csysY2] = [('IK', 0, 1, ['IK', ikTarget, 1, None, (True, False,False)])]


    def addCSysBone(self, bname, infix, boneInfo, parent, head, offs, roll):
        csys = csysBoneName(bname, infix)
        bone = boneInfo[csys] = Bone(self.armature, csys)
        bone.fromInfo((roll, parent, 0, L_HELP2))
        self.headsTails[csys] = (head, (head,offs))
        return csys


    def fixCSysBones(self, csysList):
        """
        Rotate the coordinate system bones into place.
        """

        amt = self.armature
        for bone in amt.bones.values():
            bone.calcRestMatrix()

        for bname,ikTarget in csysList:
            bone = amt.bones[bname]
            mat = bone.matrixRest

            self.fixCSysBone(bname, "_X1", mat, 0, (1,0,0), 90*D)
            self.fixCSysBone(bname, "_X2", mat, 0, (1,0,0), -90*D)
            self.fixCSysBone(bname, "_Y1", mat, 1, (0,1,0), 90*D)
            self.fixCSysBone(bname, "_Y2", mat, 1, (0,1,0), -90*D)
            self.fixCSysBone(bname, "_Z1", mat, 2, (0,0,1), 90*D)
            self.fixCSysBone(bname, "_Z2", mat, 2, (0,0,1), -90*D)


    def fixCSysBone(self, bname, infix, mat, index, axis, angle):
        csys = csysBoneName(bname, infix)
        bone = self.armature.bones[csys]
        rot = tm.rotation_matrix(angle, axis)
        cmat = np.dot(mat, rot)
        bone.tail = bone.head + self.armature.bones[bname].length * cmat[:3,1]
        normal = getUnitVector(mat[:3,index])
        bone.roll = computeRoll(bone.head, bone.tail, normal)


