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

Armature utilities
"""


#-------------------------------------------------------------------------------        
#   Utilities
#-------------------------------------------------------------------------------        


def m2b(vec):
    return np.array((vec[0], -vec[2], vec[1]))
        
def b2m(vec):
    return np.array((vec[0], vec[2], -vec[1]))
            
def getUnitVector(vec):
    length = math.sqrt(np.dot(vec,vec))
    if length > 1e-6:
        return vec/length
    else:
        return None


def splitBoneName(bone):
    words = bone.rsplit(".", 1)
    if len(words) > 1:
        return words[0], "."+words[1]
    else:
        return words[0], ""
       

def splitBonesNames(base, ext, numAfter):
    if numAfter:
        defname1 = "DEF-"+base+ext+".01"
        defname2 = "DEF-"+base+ext+".02"
        defname3 = "DEF-"+base+ext+".03"
    else:
        defname1 = "DEF-"+base+".01"+ext
        defname2 = "DEF-"+base+".02"+ext
        defname3 = "DEF-"+base+".03"+ext
    return defname1, defname2, defname3


def addDict(dict, struct):
    for key,value in dict.items():
        struct[key] = value


def mergeDicts(dicts):
    struct = {}
    for dict in dicts:   
        addDict(dict, struct)
    return struct
    
    
def safeGet(dict, key, default):
    try:
        return dict[key]
    except KeyError:
        return default
       

def copyTransform(target, cnsname, inf=1):
    return ('CopyTrans', 0, inf, [cnsname, target, 0])


def checkOrthogonal(mat):
    prod = np.dot(mat, mat.transpose())
    diff = prod - np.identity(3,float)
    sum = 0
    for i in range(3):
        for j in range(3):
            if abs(diff[i,j]) > 1e-5:
                raise NameError("Not ortho: diff[%d,%d] = %g\n%s\n\%s" % (i, j, diff[i,j], mat, prod))
    return True

#-------------------------------------------------------------------------------        
#   
#-------------------------------------------------------------------------------        

def readVertexGroups(file, vgroups, vgroupList):
    #file = os.path.join("shared/armature/vertexgroups", name)
    fp = open(file, "rU")
    for line in fp:
        words = line.split()
        if len(words) < 2:
            continue
        elif words[1] == "weights":
            name = words[2]
            try:
                vgroup = vgroups[name]
            except KeyError:
                vgroup = []
                vgroups[name] = vgroup 
            vgroupList.append((name, vgroup))
        else:
            vgroup.append((int(words[0]), float(words[1])))
    fp.close()  

    
def mergeWeights(vgroup):
    vgroup.sort()
    ngroup = []
    vn0 = -1
    w0 = 0
    for vn,w in vgroup:
        if vn == vn0:
            w0 += w
        else:
            ngroup.append((vn0,w0))
            vn0 = vn
            w0 = w
    if vn0 >= 0:
        ngroup.append((vn0,w0))
    return ngroup
    
   