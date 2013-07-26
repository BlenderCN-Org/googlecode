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

A rich mesh, with vertex weights, shapes and an armature

TODO
"""

import os
import log
import module3d

from material import Material, Color

# CStuff used by exportutils/collect. Will eventually be merged with RichMesh

class CStuff:
    def __init__(self, name, proxy, human):
        self.name = os.path.basename(name)
        self.proxy = proxy
        self.human = human
        self._richMesh = None
        if proxy:
            self.type = proxy.type
            self.material = proxy.material
            self.material.name = proxy.name + "Material"
            texture = proxy.getActualTexture(human)
            if texture is not None:
                self.material.setDiffuseTexture(texture)
        else:
            self.type = None
            self.material = human.material
            self.material.name = self.name + "Material"

    @property
    def richMesh(self):
        return self._richMesh

    @richMesh.setter
    def richMesh(self, newRichMesh):
        self._richMesh = newRichMesh
        if newRichMesh.material:
            self.material = newRichMesh.material

    def __repr__(self):
        return "<CStuff %s %s mat %s>" % (self.name, self.type, self.material)


class RichMesh:

    def __init__(self, name, amt):
        self.name = os.path.basename(name)
        self.object = None
        self.weights = {}
        self.shapes = []
        self.armature = amt
        self.material = None

        self.vertexMask = None
        self.faceMask = None
        self.vertexMapping = None   # Maps vertex index of original object to the attached filtered object


    def fromProxy(self, coords, texVerts, faceVerts, faceUvs, weights, shapes, scale=1.0):
        obj = self.object = module3d.Object3D(self.name)
        obj.setCoords(coords)
        obj.setUVs(texVerts)

        for fv in faceVerts:
            if len(fv) != 4:
                raise NameError("Mesh %s has non-quad faces and can not be handled by MakeHuman" % self.name)

        obj.createFaceGroup("Full Object")
        obj.setFaces(faceVerts, faceUvs)
        self.weights = weights
        self.shapes = shapes
        return self


    def fromObject(self, obj, weights, shapes):
        self.object = obj
        self.weights = weights
        self.shapes = shapes
        self.material = obj.material
        return self


    def rescale(self, scale):
        obj = self.object
        newobj = module3d.Object3D(self.name)
        newobj.setCoords(scale*obj.coord)
        newobj.setUVs(obj.texco)
        newobj.setFaces(obj.fvert, obj.fuvs)
        self.object = newobj

        newshapes = []
        for name,shape in self.shapes:
            newshape = {}
            for vn,dr in shape.items():
                newshape[vn] = scale*dr
            newshapes.append((name, newshape))
        self.shapes = newshapes


    def __repr__(self):
        return ("<RichMesh %s w %d t %d>" % (self.object, len(self.weights), len(self.shapes)))

    def calculateSkinWeights(self, amt):
        if self.object is None:
            raise NameError("%s has no object. Cannot calculate skin weights" % self)
        
        self.vertexWeights = [list() for _ in xrange(len(self.object.coord))]
        self.skinWeights = []

        wn = 0
        for (bn,b) in enumerate(amt.bones):
            try:
                wts = self.weights[b]
            except KeyError:
                wts = []
            for (vn,w) in wts:
                self.vertexWeights[int(vn)].append((bn,wn))
                wn += 1
            self.skinWeights.extend(wts)


def getRichMesh(obj, proxy, rawWeights, rawShapes, amt, scale=1.0):
    if proxy:
        obj = proxy.getObject()
        weights = proxy.getWeights(rawWeights)
        shapes = proxy.getShapes(rawShapes, scale)
        return RichMesh(proxy.name, amt).fromObject(obj, weights, shapes)
    else:
        return RichMesh(obj.name, amt).fromObject(obj, rawWeights, rawShapes)
