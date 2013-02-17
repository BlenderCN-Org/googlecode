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
MakeHuman to Collada (MakeHuman eXchange format) exporter. Collada files can be loaded into
Blender by collada_import.py.

TODO
"""

import module3d
import aljabr
import mh
import files3d
import mh2bvh
import os
import time
import numpy
import shutil

import export
import mh2proxy
import log
import catmull_clark_subdivision as cks

from .config import Config
from . import rig as rigfile

#
#    class CStuff
#

class CStuff:
    def __init__(self, name, proxy):
        self.name = os.path.basename(name)
        self.object = None
        self.meshInfo = None
        self.boneInfo = None
        self.vertexWeights = None
        self.skinWeights = None
        if proxy:
            self.proxy = proxy
            self.type = proxy.type
            self.material = proxy.material
            self.texture = proxy.texture
            self.specular = proxy.specular
            self.normal = proxy.normal
            self.transparency = proxy.transparency
            self.bump = proxy.bump
            self.displacement = proxy.displacement
        else:                    
            self.proxy = None
            self.type = None
            self.material = None
            self.texture = ("data/textures", "texture.png") 
            self.specular = None # ("data/textures", "texture_ref.png") 
            self.bump = None
            self.normal = None
            self.transparency = None
            self.bump = None
            self.displacement = None

            
    #def setObject3dMesh(self, object3d, weights, shapes):
    #    self.meshInfo.setObject3dMesh(object3d, weights, shapes)
        

    def __repr__(self):
        return "<CStuff %s %s mat %s tex %s>" % (self.name, self.type, self.material, self.texture)

    def hasMaterial(self):
        return (
            self.material != None or
            self.texture != None or
            self.specular != None or
            self.normal != None or
            self.transparency != None or
            self.bump != None or
            self.displacement != None)
    

class CBoneInfo:
    def __init__(self, root, heads, tails, rolls, hier, bones, weights):
        self.root = root
        self.heads = heads
        self.tails = tails
        self.rolls = rolls
        self.hier = hier
        self.bones = bones
        self.weights = weights
        
    def __repr__(self):
        return ("<CBoneInfo r %s h %d t %s r %d\n   h %s\n   b %s\n   w %s" % 
            (self.root, len(self.heads), len(self.tails), len(self.rolls), 
             self.hier, self.bones, self.weights))
       
#
#   setupObjects
#

def setupObjects(name, human, config=None, rigfile=None, rawTargets=[], helpers=False, hidden=True, eyebrows=True, lashes=True, subdivide = False, progressCallback=None):
    global theStuff, theTextures, theTexFiles, theMaterials

    def progress(base,prog):
        if progressCallback == None:
            pass
        else:
            progressCallback (base+prog)

    def getSubdivision(obj,progressCallback=None):
        if obj.isSubdivided() and not obj.isProxied():
            return obj.getSubdivisionMesh(False)
        else:
            return cks.createSubdivisionObject(obj.getSeedMesh(), progressCallback)
    
    if not config:
        config = Config()
        config.addObjects(human)
        
    obj = human.meshData
    theTextures = {}
    theTexFiles = {}
    theMaterials = {}
    
    stuffs = []
    stuff = CStuff(name, None)

    if rigfile:
        stuff.boneInfo = getArmatureFromRigFile(rigfile, obj, config.scale)
        log.message("Using rig file %s" % rigfile)
            
    meshInfo = mh2proxy.getMeshInfo(obj, None, config, None, rawTargets, None)
    if stuff.boneInfo:
        meshInfo.weights = stuff.boneInfo.weights

    theStuff = stuff
    deleteGroups = []
    if hidden:
        deleteVerts = None
    else:
        deleteVerts = numpy.zeros(len(obj.verts), bool)
    _,deleteVerts = setupProxies('Clothes', None, obj, stuffs, meshInfo, config, deleteGroups, deleteVerts)
    _,deleteVerts = setupProxies('Hair', None, obj, stuffs, meshInfo, config, deleteGroups, deleteVerts)
    foundProxy,deleteVerts = setupProxies('Proxy', name, obj, stuffs, meshInfo, config, deleteGroups, deleteVerts)
    if not foundProxy:
        # If we subdivide here, helpers will not be removed.
        # Subdiv of main mesh moved below
        if helpers:     # helpers override everything
            if config.scale == 1.0:
                stuff.meshInfo = meshInfo
            else:
                stuff.meshInfo = meshInfo.fromProxy(config.scale*obj.coord, obj.texco, obj.faces, obj.fuvs, meshInfo.weights, meshInfo.shapes)
        else:
            stuff.meshInfo = filterMesh(meshInfo, config.scale, deleteGroups, deleteVerts, eyebrows, lashes)
        stuffs = [stuff] + stuffs

    clothKeys = human.clothesObjs.keys()

    # Apply custom textures if applicable
    # TL: Clothes and Hair are now different proxy types.
    # Can probably simplify this code. Need uuid?
    for stuff in stuffs:
        proxy = stuff.proxy
        if proxy:
            if proxy.type == 'Clothes':
                uuid = proxy.getUuid()
                if uuid:
                    if uuid in clothKeys:
                        # Clothes
                        clothesObj = human.clothesObjs[uuid]
                        if clothesObj:
                            texture = clothesObj.mesh.texture
                            stuff.texture = (os.path.dirname(texture), os.path.basename(texture))
            elif proxy.type == 'Hair':
                uuid = proxy.getUuid()
                if uuid == human.hairProxy.getUuid():
                    # Hair
                    texture = human.hairObj.mesh.texture
                    stuff.texture = (os.path.dirname(texture), os.path.basename(texture))
            elif proxy.type == 'Proxy':
                # Proxy
                texture = human.mesh.texture
                stuff.texture = (os.path.dirname(texture), os.path.basename(texture))

    # Subdivide meshes if requested
    # TL: Subdivision of main mesh moved here
    if subdivide:
        for stuff in stuffs:
            proxy = stuff.proxy
            if proxy:
                if proxy.type == 'Clothes':
                    uuid = proxy.getUuid()
                    if uuid and uuid in clothKeys:
                        # Subdivide clothes
                        clo = human.clothesObjs[uuid]
                        subMesh = getSubdivision(clo)
                        stuff.meshInfo.fromObject(subMesh, stuff.meshInfo.weights, rawTargets)
                if proxy.type == 'Hair':
                    uuid = proxy.getUuid()
                    if uuid == human.hairProxy.getUuid():
                        # Subdivide hair
                        hair = human.hairObj
                        subMesh = getSubdivision(hair)
                        stuff.meshInfo.fromObject(subMesh, stuff.meshInfo.weights, rawTargets)
                elif proxy.type == 'Proxy':
                    # Subdivide proxy
                    subMesh = getSubdivision(human)
                    stuff.meshInfo.fromObject(subMesh, stuff.meshInfo.weights, rawTargets)
                    
            else:
                # Get filtered mesh
                obj = stuff.meshInfo.object
                subMesh = getSubdivision(obj, lambda p: progress(0,p*0.5))
                stuff.meshInfo.fromObject(subMesh, stuff.meshInfo.weights, rawTargets)
           

    progress(1,0)
    return stuffs

#
#    setupProxies(typename, name, obj, stuffs, meshInfo, config, deleteGroups, deleteVerts):
#

def setupProxies(typename, name, obj, stuffs, meshInfo, config, deleteGroups, deleteVerts):
    global theStuff
    
    foundProxy = False    
    for pfile in config.proxyList:
        if pfile.type == typename and pfile.file:
            proxy = mh2proxy.readProxyFile(obj, pfile, evalOnLoad=True, scale=config.scale)
            if proxy and proxy.name and proxy.texVerts:
                foundProxy = True
                deleteGroups += proxy.deleteGroups
                if deleteVerts != None:
                    deleteVerts = deleteVerts | proxy.deleteVerts
                if name:
                    stuff = CStuff(name, proxy)
                else:
                    stuff = CStuff(proxy.name, proxy)
                stuff.boneInfo = theStuff.boneInfo
                if stuff:
                    if pfile.type == 'Proxy':
                        theStuff = stuff
                    if theStuff:
                        stuffname = theStuff.name
                    else:
                        stuffname = None

                    stuff.meshInfo = mh2proxy.getMeshInfo(obj, proxy, config, meshInfo.weights, meshInfo.shapes, stuffname)

                    stuffs.append(stuff)
    return foundProxy, deleteVerts

#
#
#

def filterMesh(meshInfo, scale, deleteGroups, deleteVerts, eyebrows, lashes):
    obj = meshInfo.object

    killUvs = numpy.zeros(len(obj.texco), bool)
    killFaces = numpy.zeros(len(obj.faces), bool)
        
    if deleteVerts:
        killVerts = deleteVerts
        for f in obj.faces:
            for v in f.verts:
                if killVerts[v.idx]:
                    killFaces[f.idx] = True             
    else:
        killVerts = numpy.zeros(len(obj.verts), bool)
        
    for fg in obj.faceGroups:
        if (("joint" in fg.name) or 
            ("helper" in fg.name) or
            ((not eyebrows) and 
             (("eyebrown" in fg.name) or ("cornea" in fg.name))) or
             ((not lashes) and 
              ("lash" in fg.name)) or
             mh2proxy.deleteGroup(fg.name, deleteGroups)):
    
            for f in fg.faces:            
                killFaces[f.idx] = True
                for v in f.verts:
                    killVerts[v.idx] = True
                for vt in f.uv:                    
                    killUvs[vt] = True
     
    n = 0
    newVerts = {}
    coords = []
    for m,co in enumerate(obj.coord):
        if not killVerts[m]:
            coords.append(scale*co)
            newVerts[m] = n
            n += 1
    
    n = 0
    texVerts = []
    newUvs = {}
    for m,uv in enumerate(obj.texco):
        if not killUvs[m]:
            texVerts.append(uv)
            newUvs[m] = n
            n += 1   
    
    faceVerts = []
    faceUvs = []
    for f in obj.faces:
        if not killFaces[f.idx]:
            fverts2 = []
            fuvs2 = []
            for v in f.verts:
                fverts2.append(newVerts[v.idx])
            for uv in f.uv:
                fuvs2.append(newUvs[uv])
            faceVerts.append(fverts2)
            faceUvs.append(fuvs2)
    
    weights = {}
    if meshInfo.weights:
        for (b, wts1) in meshInfo.weights.items():
            wts2 = []
            for (v1,w) in wts1:
                if not killVerts[v1]:
                   wts2.append((newVerts[v1],w))
            weights[b] = wts2
    
    shapes = []
    if meshInfo.shapes:
        for (name, morphs1) in meshInfo.shapes:
            morphs2 = {}
            for (v1,dx) in morphs1.items():
                if not killVerts[v1]:
                    morphs2[newVerts[v1]] = scale*dx
            shapes.append((name, morphs2))

    meshInfo.fromProxy(coords, texVerts, faceVerts, faceUvs, weights, shapes)
    return meshInfo
 
#
#   getTextureNames(stuff):
#

def getTextureNames(stuff):
    global theTextures, theTexFiles, theMaterials

    if not stuff.type:
        return ("SkinShader", None, "SkinShader")
        
    try:
        texname = theTextures[stuff.name]
        texfile = theTexFiles[stuff.name]
        matname = theMaterials[stuff.name]
        return (texname, texfile, matname)
    except KeyError:
        pass
    
    texname = None
    texfile = None
    matname = None
    if stuff.texture:        
        (folder, fname) = stuff.texture
        (texname, ext) = os.path.splitext(fname)
        texfile = ("%s_%s" % (texname, ext[1:]))
        while texname in theTextures.values():
            texname = nextName(texname)
        theTextures[stuff.name] = texname
        theTexFiles[stuff.name] = texfile
    if stuff.material:
        matname = stuff.material.name
        while matname in theMaterials.values():
            matname = nextName(matname)
        theMaterials[stuff.name] = matname
    return (texname, texfile, matname)
    
    
def nextName(string):
    try:
        n = int(string[-3:])
    except:
        n = -1
    if n >= 0:
        return "%s%03d" % (string[:-3], n+1)
    else:
        return string + "_001"
        
#
#    getArmatureFromRigFile(fileName, obj, scale):    
#

def getArmatureFromRigFile(fileName, obj, scale):
    (locations, armature, weights) = rigfile.readRigFile(fileName, obj)
    
    hier = []
    heads = {}
    tails = {}
    rolls = {}
    root = None
    for (bone, head, tail, roll, parent, options) in armature:
        heads[bone] = head*scale
        tails[bone] = tail*scale
        rolls[bone] = roll
        if parent == '-':
            hier.append((bone, []))
            if root is None:
                root = bone
        else:
            parHier = findInHierarchy(parent, hier)
            try:
                (p, children) = parHier
            except:
                raise NameError("Did not find %s parent %s" % (bone, parent))
            children.append((bone, []))
    
    if root is None:
        raise NameError("No root bone found in rig file %s" % fileName)
    # newHier = addInvBones(hier, heads, tails)
    newHier = hier
    bones = []
    flatten(newHier, bones)
    return CBoneInfo(root, heads, tails, rolls, newHier, bones, weights)


def addInvBones(hier, heads, tails):
    newHier = []
    for (bone, children) in hier:
        newChildren = addInvBones(children, heads, tails)
        n = len(children)
        if n == 1:
            (child, subChildren) = children[0]
            offs = vsub(tails[bone], heads[child])
        if n > 1 or (n == 1 and vlen(offs) > 1e-4):
            boneInv = bone+"Inv"
            heads[boneInv] = tails[bone]
            #tails[boneInv] = heads[bone]
            tails[boneInv] = aljabr.vadd(tails[bone], Delta)
            newHier.append( (bone, [(boneInv, newChildren)]) )
        else:
            newHier.append( (bone, newChildren) )

    return newHier


def findInHierarchy(bone, hier):
    if hier == []:
        return []
    for pair in hier:
        (b, children) = pair
        if b == bone:
            return pair
        else:
            b = findInHierarchy(bone, children)
            if b: return b
    return []


def flatten(hier, bones):
    for (bone, children) in hier:
        bones.append(bone)
        flatten(children, bones)
    return

#
#   setStuffSkinWeights(stuff):
#

def setStuffSkinWeights(stuff):
    obj = stuff.meshInfo.object
    
    stuff.vertexWeights = {}
    for v in obj.verts:
        stuff.vertexWeights[v.idx] = []

    stuff.skinWeights = []
    wn = 0    
    for (bn,b) in enumerate(stuff.boneInfo.bones):
        try:
            wts = stuff.meshInfo.weights[b]
        except KeyError:
            wts = []
        for (vn,w) in wts:
            stuff.vertexWeights[int(vn)].append((bn,wn))
            wn += 1
        stuff.skinWeights.extend(wts)
    return
    
