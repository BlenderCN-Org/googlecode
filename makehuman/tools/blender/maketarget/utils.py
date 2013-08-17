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

"""


import bpy
import os
import math

from . import mh

Epsilon = 1e-3

#----------------------------------------------------------
#   Round targets
#----------------------------------------------------------

def round(x):
    if abs(x) < 1e-3:
        return "0"
    elif abs(x) > 10.0:
        string = "%.5g" % x
    else:
        string = "%.4g" % x
    if len(string) > 2:
        if string[:2] == "0.":
            return string[1:5]
        elif string[:3] == "-0.":
            return "-" + string[2:6]
    return string

#----------------------------------------------------------
#   Set object mode
#----------------------------------------------------------

def setObjectMode(context):
    if context.object:
        bpy.ops.object.mode_set(mode='OBJECT')

#----------------------------------------------------------
#   Common panel parts
#----------------------------------------------------------

def drawConfirm(layout, scn):
    #if not maketarget.isInited(scn):
    #    layout.operator("mh.init")
    #    return False
    if mh.confirm:
        layout.label(mh.confirmString)
        if mh.confirmString2:
           layout.label(mh.confirmString2)
        layout.operator(mh.confirm, text="Yes")
        layout.operator("mh.skip")
        return False
    return True


def skipConfirm():
    print("Skipped:", mh.confirmString)
    mh.confirm = None
    mh.confirmString = "?"
    mh.confirmString2 = None


#----------------------------------------------------------
#   Check for numpy
#----------------------------------------------------------

def checkForNumpy(layout, string):
    if not mh.foundNumpy:
        layout.label("numpy could not be loaded,")
        layout.label("either because it was not found")
        layout.label("or this is a 64-bit Blender.")
        layout.label("%s will not work" % string)
        return False
    return True

#----------------------------------------------------------
#   Try to load numpy.
#   Will only work if it is installed and for 32 bits.
#----------------------------------------------------------

#import numpy
import sys
import imp

def getModule(modname):
    try:
        return sys.modules[modname]
    except KeyError:
        pass
    print("Trying to load %s" % modname)
    fp, pathname, description = imp.find_module(modname)
    try:
        imp.load_module(modname, fp, pathname, description)
    finally:
        if fp:
            fp.close()
    return sys.modules[modname]

def getNumpy(string):
    try:
        numpy = getModule("numpy")
        mh.foundNumpy = True
        print("Numpy successfully loaded")
    except:
        numpy = None
        mh.foundNumpy = False
        print("Failed to load numpy. %s will not work" % string)
    return numpy

#----------------------------------------------------------
#   Utililies
#----------------------------------------------------------

def findBase(context):
    for ob in context.scene.objects:
        if isBase(ob):
            return ob
    raise NameError("No base object found")

def isBase(ob):
    try:
        return (ob["NTargets"] == 0)
    except:
        return False

def isTarget(ob):
    try:
        return (ob["NTargets"] > 0)
    except:
        return False

def isBaseOrTarget(ob):
    try:
        ob["NTargets"]
        return True
    except:
        return False

def deleteAll(context):
    scn = context.scene
    for ob in scn.objects:
        if isBaseOrTarget(ob):
            scn.objects.unlink(ob)
    return

def nameFromPath(filepath):
    (name,ext) = os.path.splitext(os.path.basename(filepath))
    return name


def removeShapeKeys(ob):
    if not ob.data.shape_keys:
        return
    skeys = ob.data.shape_keys.key_blocks
    n = len(skeys)
    while n >= 0:
        ob.active_shape_key_index = n
        bpy.ops.object.shape_key_remove()
        n -= 1
    return


def printVec(string, vec):
    print(string, "(%.4f %.4f %.4f)" % (vec[0], vec[1], vec[2]))


#----------------------------------------------------------
#   Get path to My Documents
#----------------------------------------------------------

def getMyDocuments():
    import sys
    if sys.platform == 'win32':
        import winreg
        try:
            k = winreg.HKEY_CURRENT_USER
            for x in ['Software', 'Microsoft', 'Windows', 'CurrentVersion', 'Explorer', 'Shell Folders']:
                k = winreg.OpenKey(k, x)

            name, type = winreg.QueryValueEx(k, 'Personal')

            if type == 1:
                print("Found My Documents folder: %s" % name)
                return name
        except Exception as e:
            print("Did not find path to My Documents folder")

    return os.path.expanduser("~")

#----------------------------------------------------------
#   loadTarget(filepath, context):
#----------------------------------------------------------

def loadTarget(filepath, context, irrelevant=[], offset=0):
    realpath = os.path.realpath(os.path.expanduser(filepath))
    fp = open(realpath, "rU")
    print("Loading target %s, ignoring: %s" % (realpath, irrelevant))

    ob = context.object
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    for v in ob.data.vertices:
        v.select = False
    name = nameFromPath(filepath)
    skey = ob.shape_key_add(name=name, from_mix=False)
    ob.active_shape_key_index = shapeKeyLen(ob) - 1
    #bpy.ops.object.shape_key_add(from_mix=False)
    #skey = ob.active_shape_key
    skey.name = name
    #print("Active", ob.active_shape_key.name)
    comments = []
    nverts = len(ob.data.vertices)
    for line in fp:
        words = line.split()
        if len(words) == 0:
            pass
        elif words[0][0] == '#':
            comments.append(line)
        else:
            index = int(words[0])

            if irrelevant:
                if isIrrelevant(index, irrelevant):
                    continue
                elif index >= irrelevant[0][0]:
                    index -= offset

            if index >= nverts:
                print("Stopped loading at index %d" % index)
                break
            dx = float(words[1])
            dy = float(words[2])
            dz = float(words[3])
            #vec = ob.data.vertices[index].co
            vec = skey.data[index].co
            if vec.length > 1e-4:
                vec[0] += dx
                vec[1] += -dz
                vec[2] += dy
                ob.data.vertices[index].select = True
    fp.close()
    skey.slider_min = -1.0
    skey.slider_max = 1.0
    skey.value = 1.0
    ob.show_only_shape_key = False
    ob.use_shape_key_edit_mode = True
    ob["NTargets"] += 1
    ob["FilePath"] = realpath
    ob["SelectedOnly"] = False
    return skey, comments


def isIrrelevant(index, irrelevant):
    for first,last in irrelevant:
        if index >= first and index < last:
            return True
    return False


def shapeKeyLen(ob):
    n = 0
    for skey in ob.data.shape_keys.key_blocks:
        n += 1
    return n