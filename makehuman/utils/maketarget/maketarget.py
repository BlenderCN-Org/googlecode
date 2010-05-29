# You may use, modify and redistribute this module under the terms of the GNU GPL.
"""
Utility function for creating a morph target (part of the development functionality).

===========================  ===============================================================
Project Name:                **MakeHuman**
Module File Location:        utils/maketarget/maketarget.py
Product Home Page:           http://www.makehuman.org/
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/
Authors:                     Manuel Bastioni
Copyright(c):                MakeHuman Team 2001-2008
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
===========================  ===============================================================

The MakeHuman application uses predefined morph target files to distort
the humanoid model when physiological changes or changes to the pose are
applied by the user. The morph target files contain extreme mesh
deformations for individual joints and features which can used
proportionately to apply less extreme deformations and which can be
combined to provide a very wide range of options to the user of the
application.

This module contains a set of functions used by 3d artists during the
development cycle to create these extreme morph target files from
hand-crafted models.

"""


__docformat__ = 'restructuredtext'

import sys
sys.path.append("/home/manuel/archive/archive_makehuman/makehuman_src/utils/svd_tools/fit")

import Blender
import math
import time
from blendersaveobj import *
try:
    import os
    from os import path
except:
    print "os module not found: some advanced functions are not available"
from Blender.BGL import *
from Blender import Draw
from Blender import Window
from Blender.Mathutils import *

import scipy
from scipy.spatial import KDTree
import numpy as np

import scan_fit
import blenderalignjoints


current_path = Blender.sys.dirname(Blender.Get('filename'))
basePath = Blender.sys.join(current_path,'base.obj')
pairsPath = Blender.sys.join(current_path,'base.sym')
centersPath = Blender.sys.join(current_path,'base.sym.centers')
morphFactor = Draw.Create(1.0)
saveOnlySelectedVerts = Draw.Create(0)
current_target = ""
loadFile = ""
targetBuffer = [] #Last target loaded
originalVerts = [] #Original base mesh coords

try:
    from topologylib import *
    import simpleoctree
except:
    print "topology libs not found"


#Some math stuff
def vsub(vect1,vect2):
    """
    This utility function returns a list of 3 float values containing the
    difference between two 3D vectors (vect1-vect2).

    Parameters
    ----------

    vect1:
        *list of floats*. A list of 3 floats containing the x, y and z
        coordinates of a vector.

    vect2:
        *list of floats*. A list of 3 floats containing the x, y and z
        coordinates of a vector.

    """
    return [vect1[0]-vect2[0], vect1[1]-vect2[1], vect1[2]-vect2[2]]

def vdist(vect1,vect2):
    """
    This utility function returns a single float value containing the
    euclidean distance between two coordinate vectors (the length of
    the line between them).

    Parameters
    ----------

    vect1:
        *list of floats*. A list of 3 floats containing the x, y and z
        coordinates of a vector.

    vect2:
        *list of floats*. A list of 3 floats containing the x, y and z
        coordinates of a vector.

    """
    joiningVect = vsub(vect1,vect2)
    return vlen(joiningVect)

def vlen(vect):
    """
    This utility function returns a single float value containing the length
    of a vector [x,y,z].

    Parameters
    ----------

    vect:
        *list of floats*. A list of 3 floats containing the x, y and z
        coordinates of a vector.

    """
    return math.sqrt(vdot(vect,vect))

def vdot(vect1,vect2):

    """
    This utility function returns a single float value containing the dot
    (scalar) product of two vectors.

    Parameters
    ----------

    vect1:
        *list of floats*. A list of 3 floats containing the x, y and z
        coordinates of a vector.

    vect2:
        *list of floats*. A list of 3 floats containing the x, y and z
        coordinates of a vector.

    """
    return vect1[0]*vect2[0] + vect1[1]*vect2[1] + vect1[2]*vect2[2]


#Starting maketarget specific functions

def doMorph(mFactor):
    """
    This function applies the currently loaded morph target to the base mesh.

    Parameters
    ----------

    mFactor:
        *float*. Morphing factor.

    """
    t1 = time.time()
    global targetBuffer
    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    obj = activeObj.getData(mesh=True)
    for vData in targetBuffer:
        mainPointIndex = vData[0]
        pointX = vData[1]
        pointY = vData[2]
        pointZ = vData[3]
        v = obj.verts[mainPointIndex]
        v.co[0] += pointX*mFactor
        v.co[1] += pointY*mFactor
        v.co[2] += pointZ*mFactor
    obj.update()
    #obj.calcNormals()
    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()
    #print "Target time", time.time() - t1
    
    
    
    
    
    
    
    
    
    
    
def alignMasks():
    """
    This function measure the similarity of 2 meshes.
    Instead to have ray intersection to measure the surfaces differences,
    we subdivide the mesh2, in order to in increase the density, and then
    we use the vert to vert distance.
    """

    print "align"
    
    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    activeObjs = Blender.Object.GetSelected()
    
    mask_scan_obj = Blender.Object.Get("mask_scan")
    mask_mh_obj = Blender.Object.Get("mask_mh")
    scan_obj = Blender.Object.Get("scan")
    
    mask_scan_data = mask_scan_obj.getData(mesh=True)
    mask_mh_data = mask_mh_obj.getData(mesh=True)
    scan_data = scan_obj.getData(mesh=True)

    mask_scan = [[v.co[0],v.co[1],v.co[2]] for v in mask_scan_data.verts]
    mask_mh = [[v.co[0],v.co[1],v.co[2]] for v in mask_mh_data.verts]
    scan = [[v.co[0],v.co[1],v.co[2]] for v in scan_data.verts]
    
    aligned_verts = scan_fit.align_scan(mask_scan,mask_mh,scan)  
    aligned_mask = scan_fit.align_scan(mask_scan,mask_mh,mask_scan)  
    
    for i,v in enumerate(aligned_verts):
        scan_data.verts[i].co[0] = v[0]
        scan_data.verts[i].co[1] = v[1]
        scan_data.verts[i].co[2] = v[2]
        
    for i,v in enumerate(aligned_mask):
        mask_scan_data.verts[i].co[0] = v[0]
        mask_scan_data.verts[i].co[1] = v[1]
        mask_scan_data.verts[i].co[2] = v[2]
        
    scan_data.update()
    mask_scan_data.update()
    
    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

def linkMask(filePath, subdivide = None):
    """
    This function measure the similarity of 2 meshes.
    Instead to have ray intersection to measure the surfaces differences,
    we subdivide the mesh2, in order to in increase the density, and then
    we use the vert to vert distance.
    """

    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    activeObjs = Blender.Object.GetSelected()
    activeObj1 = activeObjs[0]#The mask must be latest selected obj
    activeObj2 = activeObjs[1]
    obj1 = activeObj1.getData(mesh=True)
    obj2 = activeObj2.getData(mesh=True)

    vertsList1 = [[v.co[0],v.co[1],v.co[2]] for v in obj1.verts]
    vertsList2 = []
    vertsList2_index = []
    for v in obj2.verts:
        if v.sel == 1:
            vertsList2_index.append(v.index)
            vertsList2.append([v.co[0],v.co[1],v.co[2]])

    #scipy code
    kd = KDTree(vertsList2)
    dists,indx = kd.query(vertsList1)
    indx = [vertsList2_index[i] for i in indx]
    dist = np.array(dists).mean()

    try:
        fileDescriptor = open(filePath, "w")
    except:
        print "Unable to open %s",(filePath)
        return  None

    for i1,i2 in enumerate(indx):
        fileDescriptor.write("%d %d\n" % (i1,i2))
    fileDescriptor.close()
    
    for v in obj2.verts:
        v.sel = 0
    
    for i in indx:
       obj2.verts[i].sel = 1 


    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()




def linkMaskBug(filePath, subdivide = None):
    """
    This function measure the similarity of 2 meshes.
    Instead to have ray intersection to measure the surfaces differences,
    we subdivide the mesh2, in order to in increase the density, and then
    we use the vert to vert distance.
    """

    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    activeObjs = Blender.Object.GetSelected()
    activeObj1 = activeObjs[0]#The mask must be latest selected obj
    activeObj2 = activeObjs[1]
    obj1 = activeObj1.getData(mesh=True)
    obj2 = activeObj2.getData(mesh=True)

    vertsList1 = [[v.co[0],v.co[1],v.co[2],v.index] for v in obj1.verts]
    vertsList2 = []
    for v in obj2.verts:
        if v.sel == 1:
            vertsList2.append([v.co[0],v.co[1],v.co[2],v.index])

    #vertsList2 = [[v.co[0],v.co[1],v.co[2]] for v in obj2.verts]
    faces = [[v.index for v in f.verts] for f in obj2.faces]

    if subdivide:
        vertsList2toProcess = subdivideObj(faces, vertsList2, 2)[1]
    vertsList2toProcess = vertsList2

    indexList = xrange(len(vertsList1))

    #We need to add index information to each vert.
    #for i,v in enumerate(vertsList2toProcess):
    #    v.append(i)

    #Init of the octree
    octree = simpleoctree.SimpleOctree(vertsList2toProcess, .25)

    #For each vert of new mesh we found the nearest verts of old one
    linked = []
    for i1 in indexList:
        v1 = vertsList1[i1]

        #We use octree to search only on a small part of the whole old mesh.
        vertsList3 = octree.root.getSmallestChild(v1)

        #... find nearest verts on old mesh
        i2 = 0
        dMin = 100
        for v2 in vertsList3.verts:
            d = vdist(v1, v2)
            if d < dMin:
                dMin = d
                i2 = v2[3]
                print dMin
        linked.append([i1,i2])



        print"Linking verts: %.2f%c."%((float(i1)/len(vertsList1))*100, "%")


    try:
        fileDescriptor = open(filePath, "w")
    except:
        print "Unable to open %s",(filePath)
        return  None

    for data in linked:
        fileDescriptor.write("%d %d\n" % (data[0],data[1]))
    fileDescriptor.close()

    for v in obj2.verts:
        v.sel = 0
    
    for i in linked:
       obj2.verts[i[1]].sel = 1 

    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()





def fitMesh(subdivide = None):
    """
    This function measure the similarity of 2 meshes.
    Instead to have ray intersection to measure the surfaces differences,
    we subdivide the mesh2, in order to in increase the density, and then
    we use the vert to vert distance.
    """

    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    activeObjs = Blender.Object.GetSelected()
    activeObj1 = activeObjs[0]#The base mesh must be latest selected
    activeObj2 = activeObjs[1]
    obj1 = activeObj1.getData(mesh=True)
    obj2 = activeObj2.getData(mesh=True)


    vertsList1 = []
    for v in obj1.verts:
        if v.sel == 1:
            vertsList1.append([v.co[0],v.co[1],v.co[2],v.index])
    vertsList2 = [[v.co[0],v.co[1],v.co[2],v.index] for v in obj2.verts]

    #vertsList2 = [[v.co[0],v.co[1],v.co[2]] for v in obj2.verts]
    faces = [[v.index for v in f.verts] for f in obj2.faces]

    if subdivide:
        vertsList2toProcess = subdivideObj(faces, vertsList2, 2)[1]
    vertsList2toProcess = vertsList2



    #We need to add index information to each vert.
    #for i,v in enumerate(vertsList2toProcess):
    #    v.append(i)

    #Init of the octree
    octree = simpleoctree.SimpleOctree(vertsList2toProcess, .25)

    #For each vert of new mesh we found the nearest verts of old one
    linked = []
    for v1 in vertsList1:

        i1 = v1[3]
        #We use octree to search only on a small part of the whole old mesh.
        vertsList3 = octree.root.getSmallestChild(v1)

        #... find nearest verts on old mesh
        i2 = 0
        dMin = 100
        for v2 in vertsList3.verts:
            d = vdist(v1, v2)
            if d < dMin:
                dMin = d
                i2 = v2[3]

        linked.append([i1,i2])



        print"Linking verts: %.2f%c."%((float(i1)/len(vertsList1))*100, "%")

    for l in linked:
        obj1.verts[l[0]].co[0] = obj2.verts[l[1]].co[0]
        obj1.verts[l[0]].co[1] = obj2.verts[l[1]].co[1]
        obj1.verts[l[0]].co[2] = obj2.verts[l[1]].co[2]

    obj1.update()
    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()







def generateTargetsDB(filepath):
    #Because Blender filechooser return a file
    #it's needed to extract the dirname

    folderToScan = os.path.dirname(filepath)

    folderToScanMoveX = os.path.join(folderToScan,"movex")
    folderToScanMoveY = os.path.join(folderToScan,"movey")
    folderToScanMoveZ = os.path.join(folderToScan,"movez")

    folderToScanScaleX = os.path.join(folderToScan,"scalex")
    folderToScanScaleY = os.path.join(folderToScan,"scaley")
    folderToScanScaleZ = os.path.join(folderToScan,"scalez")
    folderToScanTypes = os.path.join(folderToScan,"types")

    targetListMoveX = os.listdir(folderToScanMoveX)
    targetListMoveY = os.listdir(folderToScanMoveY)
    targetListMoveZ = os.listdir(folderToScanMoveZ)
    targetListScaleX = os.listdir(folderToScanScaleX)
    targetListScaleY = os.listdir(folderToScanScaleY)
    targetListScaleZ = os.listdir(folderToScanScaleZ)
    targetListTypes = os.listdir(folderToScanTypes)

    counter = 0
    for tp in targetListTypes:
        for mx in targetListMoveX:
            for my in targetListMoveY:
                for mz in targetListMoveZ:
                    for sx in targetListScaleX:
                        for sy in targetListScaleY:
                            for sz in targetListScaleZ:
                                print "Iteration %s"%(counter)

                                n1 =os.path.splitext(mx)[0]
                                n2 =os.path.splitext(my)[0]
                                n3 =os.path.splitext(mz)[0]
                                n4 =os.path.splitext(sx)[0]
                                n5 =os.path.splitext(sy)[0]
                                n6 =os.path.splitext(sz)[0]
                                n7 =os.path.splitext(tp)[0]

                                t = "%s-%s-%s-%s-%s-%s-%s"%(n1,n2,n3,n4,n5,n6,n7)

                                moveX = os.path.join(folderToScanMoveX,mx)
                                moveY = os.path.join(folderToScanMoveY,my)
                                moveZ = os.path.join(folderToScanMoveZ,mz)
                                scaleX = os.path.join(folderToScanScaleX,sx)
                                scaleY = os.path.join(folderToScanScaleY,sy)
                                scaleZ = os.path.join(folderToScanScaleZ,sz)
                                type = os.path.join(folderToScanTypes,tp)

                                loadTranslationTarget(type)
                                doMorph(1)
                                loadTranslationTarget(moveX)
                                doMorph(1)
                                loadTranslationTarget(moveY)
                                doMorph(1)
                                loadTranslationTarget(moveZ)
                                doMorph(1)
                                loadTranslationTarget(scaleX)
                                doMorph(1)
                                loadTranslationTarget(scaleY)
                                doMorph(1)
                                loadTranslationTarget(scaleZ)
                                doMorph(1)
                                newTargetPath = os.path.join(folderToScan,t+".target")
                                saveTranslationTarget(newTargetPath)
                                resetMesh()
                                counter += 1


def maskComparison(vertsList1, vertsList2, linkMaskBaseIndices,linkMaskClientIndices):
    """
    This function measure the similarity of 2 meshes.
    Instead to have ray intersection to measure the surfaces differences,
    we subdivide the mesh2, in order to in increase the density, and then
    we use the vert to vert distance.
    """







    #For each vert of base Mask we found the nearest verts of scan Mask
    vDistances = []
    dSum = 0
    for i in xrange(len(linkMaskBaseIndices)):
        i1 = linkMaskBaseIndices[i]
        i2 = linkMaskClientIndices[i]
        v1 = vertsList1[i1]
        v2 = vertsList2[i2]
        dst = vdist(v1, v2)
        vDistances.append(dst)
        dSum += dst


    averageDist = dSum/len(vDistances)

    return averageDist


def meshComparison(indexListPath, subdivide = None):
    """
    This function measure the similarity of 2 meshes.
    Instead to have ray intersection to measure the surfaces differences,
    we subdivide the mesh2, in order to in increase the density, and then
    we use the vert to vert distance.
    """

    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    activeObjs = Blender.Object.GetSelected()
    activeObj1 = activeObjs[0]
    activeObj2 = activeObjs[1]
    obj1 = activeObj1.getData(mesh=True)
    obj2 = activeObj2.getData(mesh=True)

    vertsList1 = [[v.co[0],v.co[1],v.co[2]] for v in obj1.verts]
    vertsList2 = [[v.co[0],v.co[1],v.co[2]] for v in obj2.verts]
    faces = [[v.index for v in f.verts] for f in obj2.faces]

    if subdivide:
        vertsList2toProcess = subdivideObj(faces, vertsList2, 2)[1]
    vertsList2toProcess = vertsList2

    if indexListPath:
        indexList = []
        try:
            fileDescriptor = open(indexListPath)
        except:
            print 'Error opening %s file' % indexListPath
            return
        for data in fileDescriptor:
            lineData = data.split()
            i = int(lineData[0])
            indexList.append(i)
        fileDescriptor.close()
    else:
        indexList = xrange(len(vertsList1))

    overwrite = 0 #Just for more elegant one-line print output progress

    #Init of the octree
    octree = simpleoctree.SimpleOctree(vertsList2toProcess, .25)

    #For each vert of new mesh we found the nearest verts of old one
    vDistances = []
    for i1 in indexList:
        v1 = vertsList1[i1]

        #We use octree to search only on a small part of the whole old mesh.
        vertsList3 = octree.root.getSmallestChild(v1)

        #... find nearest verts on old mesh
        dMin = 100
        for v2 in vertsList3.verts:
            d = vdist(v1, v2)
            if d < dMin:
                dMin = d
        vDistances.append(dMin)

        word = "Linking verts: %.2f%c."%((float(i1)/len(vertsList1))*100, "%")
        sys.stdout.write("%s%s\r" % (word, " "*overwrite ))
        sys.stdout.flush()
        overwrite = len(word)

    dSum = 0
    for d in vDistances:
        dSum += d

    averageDist = dSum/len(vDistances)
    print "Average distance = %s"%(averageDist)
    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()
    return averageDist


def findCloserMesh(filepath):
    #Because Blender filechooser return a file
    #it's needed to extract the dirname

    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    activeObjs = Blender.Object.GetSelected()
    activeObj1 = activeObjs[0]#The base must be latest selected obj
    activeObj2 = activeObjs[1]
    obj1 = activeObj1.getData(mesh=True)
    obj2 = activeObj2.getData(mesh=True)


    vertsList2 = [[v.co[0],v.co[1],v.co[2]] for v in obj2.verts]

    linkMaskBaseIndices = []
    linkMaskClientIndices = []

    try:
        fileDescriptor = open("mask.linked")
    except:
        print 'Error opening %s file' % "mask.linked"
        return
    for data in fileDescriptor:
        lineData = data.split()
        i = int(lineData[1])
        linkMaskBaseIndices.append(i)
    fileDescriptor.close()

    try:
        fileDescriptor = open("temp.linked")
    except:
        print 'Error opening %s file' % "temp.linked"
        return
    for data in fileDescriptor:
        lineData = data.split()
        i = int(lineData[1])
        linkMaskClientIndices.append(i)
    fileDescriptor.close()

    folderToScan = os.path.dirname(filepath)
    targetList = os.listdir(folderToScan)
    results = {}

    val = 0.2

    for targetName in targetList:
        targetPath = os.path.join(folderToScan,targetName)
        loadTranslationTarget(targetPath)
        doMorph(val)
        vertsList1 = [[v.co[0],v.co[1],v.co[2]] for v in obj1.verts]
        n = maskComparison(vertsList1, vertsList2, linkMaskBaseIndices,linkMaskClientIndices)
        print n
        results[n] = targetPath
        doMorph(-val)
    dKeys = results.keys()
    dKeys.sort()

    if dKeys[0] > 0.05:
        val = 1.0
        for targetName in targetList:
            targetPath = os.path.join(folderToScan,targetName)
            loadTranslationTarget(targetPath)
            doMorph(val)
            vertsList1 = [[v.co[0],v.co[1],v.co[2]] for v in obj1.verts]
            n = maskComparison(vertsList1, vertsList2, linkMaskBaseIndices,linkMaskClientIndices)
            #print targetPath,n
            results[n] = targetPath
            doMorph(-val)
    #dKeys = results.keys()
    dKeys.sort()
    closerTarget = results[dKeys[0]]



    loadTranslationTarget(closerTarget)
    doMorph(val)


    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()
    print "Closer target = %s, %s"%(closerTarget,dKeys[0])






def loadTranslationTarget(targetPath):
    """
    This function loads a morph target file.

    Parameters
    ----------

    targetPath:
        *string*. A string containing the operating system path to the
        file to be read.

    """
    global targetBuffer,current_target
    try:
        fileDescriptor = open(targetPath)
    except:
        Draw.PupMenu("Unable to open %s",(targetPath))
        return  None
    activeObjs = Blender.Object.GetSelected()
    if len(activeObjs) > 0:
        activeObj = activeObjs[0]
    else:
        Draw.PupMenu("No object selected")
        return None

    obj = activeObj.getData(mesh=True)
    try:
        obj.verts
    except:
        Draw.PupMenu("The selected obj is not a mesh")
        return None

    #check mesh version
    if len(obj.verts) == 11787:
        print "Working on Mesh MH1.0.0prealpha"
        if len(obj.verts) < 11787:
            Draw.PupMenu("The selected obj is not last version of MHmesh")
            if len(obj.verts) == 11751:
                print "Working on Mesh MH0.9.2NR"
            elif len(obj.verts) < 11751:
                print "Working on Mesh 0.9.1 or earlier"


    current_target = targetPath
    targetData = fileDescriptor.readlines()
    fileDescriptor.close()
    targetBuffer = []
    maxIndexOfVerts = len(obj.verts)
    for vData in targetData:
        vectorData = vData.split()
        if vectorData[0].find('#')==-1:
            if len(vectorData) < 4:
                vectorData = vData.split(',') #compatible old format
            mainPointIndex = int(vectorData[0])
            if mainPointIndex < maxIndexOfVerts:
                pointX = float(vectorData[1])
                pointY = float(vectorData[2])
                pointZ = float(vectorData[3])
                targetBuffer.append([mainPointIndex, pointX,pointY,pointZ])
            #else:
            #    Draw.PupMenu("WARNING: target has more verts than Base mesh")
    return 1

def saveTranslationTarget(targetPath):
    """
    This function saves a morph target file containing the difference between
    the *originalVerts* positions and the actual vertex coordinates.

    Parameters
    ----------

    targetPath:
        *string*. A string containing the operating system path to the
        file to be written.

    epsilon:
        *float*. The max value of difference between original vert and
        actual vert. If the distance is over epsilon, the vert is
        considered as modificated, so to save as target morph.
        ** EDITORIAL NOTE** This parameter is not implemented.

    """

    global originalVerts
    global saveOnlySelectedVerts
    onlySelection = saveOnlySelectedVerts.val
    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    epsilon = 0.001
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    obj = activeObj.getData(mesh=True)
    #obj = Mesh.Get("Base")
    modifiedVertsIndices = []
    groupToSave = None #TODO
    if not groupToSave:
        vertsToSave = range(len(obj.verts))
    else:
        pass #TODO verts from group

    nVertsExported = 0
    for index in vertsToSave:
        originalVertex = originalVerts[index]
        targetVertex = obj.verts[index]
        delta = vsub(targetVertex.co,originalVertex)
        dist =  vdist(originalVertex,targetVertex.co)
        if dist > epsilon:
            nVertsExported += 1
            dataToExport =  [index,delta[0],delta[1],delta[2]]
            if onlySelection == 1:
                if targetVertex.sel == 1:
                    modifiedVertsIndices.append(dataToExport)
            else:
                modifiedVertsIndices.append(dataToExport)

    try:
        fileDescriptor = open(targetPath, "w")
    except:
        print "Unable to open %s",(targetPath)
        return  None

    for data in modifiedVertsIndices:
        fileDescriptor.write("%d %f %f %f\n" % (data[0],data[1],data[2],data[3]))
    fileDescriptor.close()

    if nVertsExported == 0:
        print "Warning%t|Zero verts exported in file "+targetPath

    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()


def saveIndexSelectedVerts(filePath):
    """
    This function saves the indices of selected verts

    Parameters
    ----------

    filePath:
        *string*. A string containing the operating system path to the
        file to be written.

    """

    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    obj = activeObj.getData(mesh=True)

    try:
        fileDescriptor = open(filePath, "w")
    except:
        print "Unable to open %s",(filePath)
        return  None

    nVertsExported = 0
    for index in xrange(len(obj.verts)):
        if obj.verts[index].sel == 1:
            fileDescriptor.write("%d\n"%(index))
    fileDescriptor.close()

    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()



def saveTranslationTargetAndHisSymm(targetPath):
    """
    This function saves a morph target file and his symmetric.
    In example, saving l-ear-move-up.target, will be automatically
    calculated and saved r-ear-move-up.target

    Parameters
    ----------

    targetPath:
        *string*. A string containing the operating system path to the
        file to be written. Must start with "l-" prefix.

    """

    saveTranslationTarget(targetPath)
    loadSymVertsIndex(1)
    loadTranslationTarget(targetPath)
    pathParts = os.path.split(targetPath)
    headPath = pathParts[0]
    tailPath = pathParts[1]
    nameSuffix = tailPath[1:]
    targetPath = os.path.join(headPath,"r"+nameSuffix)
    doMorph(-1)
    saveTranslationTarget(targetPath)
    resetMesh()

def loadAllTargetInFolder(filepath):
    #Because Blender filechooser return a file
    #it's needed to extract the dirname
    folderToScan = os.path.dirname(filepath)
    targetList = os.listdir(folderToScan)
    for targetName in targetList:
        targetPath = os.path.join(folderToScan,targetName)
        loadTranslationTarget(targetPath)
        doMorph(0.5)


def utility1(filepath,basetype= "mc"):
    """
    This function is used to adjust little changes on base
    meshes, correcting all targets
    """


    folderToScan = os.path.dirname(filepath)
    oldBasesPath = os.path.join(folderToScan,"oldbases")
    newBasesPath = os.path.join(folderToScan,"newbases")
    targetList = os.listdir(folderToScan)

    if basetype == "fc":
        oldBase = os.path.join(oldBasesPath,"neutral-female-child.target")
        newBase = os.path.join(newBasesPath,"neutral-female-child.target")
    elif basetype == "fy":
        oldBase = os.path.join(oldBasesPath,"neutral-female-young.target")
        newBase = os.path.join(newBasesPath,"neutral-female-young.target")
    elif basetype == "fo":
        oldBase = os.path.join(oldBasesPath,"neutral-female-old.target")
        newBase = os.path.join(newBasesPath,"neutral-female-old.target")
    elif basetype == "mc":
        oldBase = os.path.join(oldBasesPath,"neutral-male-child.target")
        newBase = os.path.join(newBasesPath,"neutral-male-child.target")
    elif basetype == "my":
        oldBase = os.path.join(oldBasesPath,"neutral-male-young.target")
        newBase = os.path.join(newBasesPath,"neutral-male-young.target")
    elif basetype == "mo":
        oldBase = os.path.join(oldBasesPath,"neutral-male-old.target")
        newBase = os.path.join(newBasesPath,"neutral-male-old.target")


    for targetName in targetList:
        targetPath = os.path.join(folderToScan,targetName)
        if os.path.isfile(targetPath):
            print "Processing %s"%(targetPath)
            loadTranslationTarget(oldBase)
            doMorph(1.0)
            loadTranslationTarget(targetPath)
            doMorph(1.0)
            loadTranslationTarget(newBase)
            doMorph(-1.0)
            saveTranslationTarget(targetPath)
            resetMesh()

def utility2(targetPath):

    print targetPath
    isModified = False
    if os.path.isfile(targetPath):
        try:
            fileDescriptor = open(targetPath)
        except:
            Draw.PupMenu("Unable to open %s",(targetPath))
            return  None
        targetData = fileDescriptor.readlines()
        fileDescriptor.close()
        targetData2 = []
        for vData in targetData:
            vectorData = vData.split()
            if vectorData[0].find('#')==-1:
                vectorData[0] = int(vectorData[0])
                if vectorData[0] > 15081:
                    isModified = True
                    vectorData[0] = vectorData[0]-428
                targetData2.append(vectorData)

    if isModified == True:
        try:
            fileDescriptor = open(targetPath, "w")
        except:
            print "Unable to open %s",(targetPath)
            return  None

        for vData in targetData2:
            fileDescriptor.write("%d %s %s %s\n" % (vData[0],vData[1],vData[2],vData[3]))
        fileDescriptor.close()

    return 1


def utility3(filepath):
    #Because Blender filechooser return a file
    #it's needed to extract the dirname
    folderToScan = os.path.dirname(filepath)
    targetList = os.listdir(folderToScan)
    for targetName in targetList:
        targetPath = os.path.join(folderToScan,targetName)
        utility2(targetPath)





def utility5(filepath):
    """
    This function is used to adjust little changes on base
    meshes, correcting all targets
    """

    folderToScan = os.path.dirname(filepath)
    fileName = os.path.basename(filepath)

    targetList = os.listdir(folderToScan)

    for targetName in targetList:
        targetPath = os.path.join(folderToScan,targetName)
        objFileName = os.path.splitext(targetName)[0]+".obj"
        objPath = os.path.join(folderToScan,objFileName)
        if os.path.isfile(targetPath):
            print "Processing %s"%(targetPath)
            loadTranslationTarget(targetPath)
            doMorph(1.0)
            saveObj(objPath)
            doMorph(-1.0)


def utility4(filepath):
    """
    This function is used to adjust little changes on base
    meshes, correcting all targets
    """


    folderToScan = os.path.dirname(filepath)
    targetList = os.listdir(folderToScan)

    for targetName in targetList:
        targetPath = os.path.join(folderToScan,targetName)
        if os.path.isfile(targetPath):
            print "Processing %s"%(targetPath)
            loadTranslationTarget(targetPath)

            doMorph(1.0)

            saveTranslationTarget(targetPath)


            doMorph(-1.0)
            
def utility6(filepath):
    """
    This function is used to adjust little changes on base
    meshes, correcting all targets
    """


    folderToScan = os.path.dirname(filepath)
    targetList = os.listdir(folderToScan)

    for targetName in targetList:
        targetPath = os.path.join(folderToScan,targetName)
        if os.path.isfile(targetPath):
            print "Processing %s"%(targetPath)
            loadTranslationTarget(targetPath)
            doMorph(1.0)
            blenderalignjoints.loadJointDelta("data.joints")

            

            saveTranslationTarget(targetPath)


            doMorph(-1.0)





def loadInitialBaseCoords(path):
    """
    This function is a little utility function to load only the vertex data
    from a wavefront obj file.

    Parameters
    ----------

    path:
        *string*. A string containing the operating system path to the
        file that contains the wavefront obj.

    """
    try:
        fileDescriptor = open(path)
    except:
        print "Error opening %s file"%(path)
        return
    data = fileDescriptor.readline()
    vertsCoo = []
    while data:
        dataList = data.split()
        if dataList[0] == "v":
            co = (float(dataList[1]),\
                    float(dataList[2]),\
                    float(dataList[3]))
            vertsCoo.append(co)
        data = fileDescriptor.readline()
    fileDescriptor.close()
    return vertsCoo


def saveSymVertsIndices(filePath):
    """
    This function identifies and saves symmetric pairs of vertices.
    If a symmetric vertex is not found, the lone vertex is selected
    and processing is halted so that the problem can be fixed.

    Parameters
    ----------

    filePath:
        *string*. A string containing the operating system path to the
        file that will contain the new or updated morph target.

    """

    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    data = activeObj.getData(mesh=True)
    leftVerts = []
    rightVerts = []
    listOfSymmIndex = []
    listOfCentralIndex = []
    for v in data.verts:
        if abs(v.co[0]) > 0.001:
            if v.co[0] < 0:
                leftVerts.append(v)
            if v.co[0] > 0:
                rightVerts.append(v)
        else:
            listOfCentralIndex.append(v.index)
    print "left verts, right verts, central verts"
    print "---------------------------------------"
    print len(leftVerts),len(rightVerts),len(listOfCentralIndex)
    print "sum: ",len(leftVerts)+len(rightVerts)+len(listOfCentralIndex)
    progress = 0.0
    progress2 = len(leftVerts)
    Window.DrawProgressBar(0, "Start")

    for v1 in leftVerts:
        v1.sel = 0
        v1Flipped = [-v1.co[0],v1.co[1],v1.co[2]]
        delta = 0.00001
        isFoundSymm = 0
        progress += 1.0
        Window.DrawProgressBar((progress/progress2), str(progress/progress2))

        while isFoundSymm == 0:
            for v2 in rightVerts:
                if vdist(v1Flipped,v2.co) < delta:

                    listOfSymmIndex.append([v1.index,v2.index])
                    rightVerts.remove(v2)
                    isFoundSymm = 1
                    break
            delta += 0.0001
            if delta > 0.005:
                print "WARNING: nos sym found", vdist(v1Flipped,v2.co),delta,v1.index,v2.index
                v1.sel = 1
                break

    Window.DrawProgressBar(1, "Done")
    file = open(filePath, 'w')
    for couple in listOfSymmIndex:
        file.write(str(couple[0]) + "," +str(couple[1]) + "\n")
    file.close()
    file = open(filePath+".centers", 'w')
    for index in listOfCentralIndex:
        file.write(" %i \n"%(index))
    file.close()
    data.update()

def loadSymVertsIndex(right=1):
    """
    Make the mesh symmetrical by reflecting the existing vertices across
    to the left or right. By default this function reflects left to right.

    Parameters
    ----------

    right:
        *int*. A flag to indicate whether the new vertices will be reflected
        across to the left or right. (1=right, 0=left)

    """

    global pairsPath
    global centersPath
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    data = activeObj.getData(mesh=True)
    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    try:
        symmFile = open(pairsPath)
    except:
        print"File Sym not found"
        return 0
    for symmCouple in symmFile:
        leftVert = data.verts[int(symmCouple.split(',')[0])]
        rightVert = data.verts[int(symmCouple.split(',')[1])]
        if right == 1:
            rightVert.co[0] = -1*(leftVert.co[0])
            rightVert.co[1] = leftVert.co[1]
            rightVert.co[2] = leftVert.co[2]
        else:
            leftVert.co[0] = -1*(rightVert.co[0])
            leftVert.co[1] = rightVert.co[1]
            leftVert.co[2] = rightVert.co[2]
    symmFile.close()

    try:
        centerFile = open(centersPath)
    except:
        print"File Sym not found"
        return 0
    for i in centerFile:
        data.verts[int(i)].co[0] = 0.0
    symmFile.close()
    data.update()
    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()


def selectSymmetricVerts():
    """
    Select symmetrical verts  by reflecting the existing selection across
    to the left or right. This function reflects left to right.

    Parameters
    ----------

    right:
        *int*. A flag to indicate whether the new vertices will be reflected
        across to the left or right. (1=right, 0=left)

    """

    global pairsPath
    print "selecting symm"
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    data = activeObj.getData(mesh=True)
    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    try:
        symmFile = open(pairsPath)
    except:
        print"File Sym not found"
        return 0
    for symmCouple in symmFile:
        leftVert = data.verts[int(symmCouple.split(',')[0])]
        rightVert = data.verts[int(symmCouple.split(',')[1])]

        if leftVert.sel == 1:
            leftVert.sel = 0
            rightVert.sel = 1
    symmFile.close()

    data.update()
    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()


def selectVerts(listOfIndices):
    """


    """

    global pairsPath
    print "selecting symm"
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    data = activeObj.getData(mesh=True)
    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    for i in listOfIndices:
        vertToSelect = data.verts[i]
        vertToSelect.sel = 1


    data.update()
    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()


def resetMesh():
    """
    This function restores the initial base mesh coordinates.

    **Parameters:** This method has no parameters.

    """
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    actual_mesh = activeObj.getData(mesh=True)
    global originalVerts
    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)
    for pointIndex, vCoords in enumerate(originalVerts):
        actual_mesh.verts[pointIndex].co[0] = vCoords[0]
        actual_mesh.verts[pointIndex].co[1] = vCoords[1]
        actual_mesh.verts[pointIndex].co[2] = vCoords[2]
    actual_mesh.update()
    actual_mesh.calcNormals()
    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()


def absoluteToRelative(path):
    """
    It resave all targets in path from absolute (it mean
    the targets are referred to base neutral mesh) from relative (it mean the
    targets are referred to a different morph of base mesh). In example
    the target female_young_nilotid is saved not from base mesh, but from
    female_young. In other words, it's needed to apply female_young before apply
    female_young_nilotid.

    Parameters
    ----------

    path:
      *path*.  Path of folder to examine.
    """
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    data = activeObj.getData(mesh=True)
    path = os.path.split(path)[0]

    targetsFiles = os.listdir(path)
    targetsNames = []
    for targetFile in targetsFiles:
        if targetFile != "base_female.target" and \
            targetFile != "base_male.target":

            #targetFile != "base_female_child.target" and \
            #targetFile != "base_male_child.target" and \
            #targetFile != "base_female_old.target" and \
            #targetFile != "base_male_old.target":
            fileName = os.path.splitext(targetFile)
            targetName = fileName[0]
            targetPath = os.path.join(path, targetFile)
            if "female" in targetName:
                absoluteTarget = os.path.join(path,"base_female.target")
            else:
                absoluteTarget = os.path.join(path,"base_male.target")
            loadTranslationTarget(targetPath)
            doMorph(1.0)
            loadTranslationTarget(absoluteTarget)
            doMorph(-1.0)
            saveTranslationTarget(targetPath)#Note it overwrite
            resetMesh()

originalVerts = loadInitialBaseCoords(basePath)







def draw():
    """
    This function draws the morph target on the screen and adds buttons to
    enable utility functions to be called to process the target.

    **Parameters:** This method has no parameters.

    """
    global targetPath,morphFactor,rotVal,rotSum,current_target,selAxis
    global saveOnlySelectedVerts

    glClearColor(0.5, 0.5, 0.5, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.0, 0.0, 0.0)
    glRasterPos2i(10, 150)
    Draw.Text("Make MH targets v2.2")
    glRasterPos2i(10, 140)
    Draw.Text("_____________________________________________")
    glRasterPos2i(10, 120)

    Draw.Button("Align", 20, 10, 150, 50, 20, "Align scans")

    Draw.Button("Load", 2, 10, 100, 50, 20, "Load target")
    Draw.Button("Morph", 3, 60, 100, 50, 20, "Morph "+current_target.replace(current_path,""))
    Draw.Button("<=", 5, 110, 100, 30, 20, "Make left side symetrical to right side")
    Draw.Button("Reset", 10, 140, 100, 40, 20, "Return base object to its original state")
    Draw.Button("=>", 6, 180, 100, 30, 20, "Make right side symetrical to left side")
    morphFactor = Draw.Number("Value: ", 0, 10, 80, 100, 20, morphFactor.val, -1, 1, "Insert the value to apply the target")
    Draw.Button("Save", 1, 110, 80, 100, 20, "Save target")
    saveOnlySelectedVerts = Draw.Toggle("Save only selected verts",0,10,60,200,20,saveOnlySelectedVerts.val,"The target will affect only the selected verts")


def event(event, value):
    """
    This function handles keyboard events when the escape key or the 's' key
    is pressed to exit or save the morph target file.

    Parameters
    ----------

    event:
        *int*. An indicator of the event to be processed
    value:
        *int*. A value **EDITORIAL NOTE: Need to find out what this is used for**

    """
    if event == Draw.ESCKEY and not value: Draw.Exit()
    elif event == Draw.SKEY:
        Window.FileSelector (saveSymVertsIndices, "Save Symm data")
    elif event == Draw.DKEY:
        selectSymmetricVerts()
    elif event == Draw.TKEY:
        Window.FileSelector (saveTranslationTargetAndHisSymm, "Save Target")
    elif event == Draw.LKEY:
        Window.FileSelector (loadAllTargetInFolder, "Load from folder")
    elif event == Draw.CKEY:
        alignMasks()
    elif event == Draw.HKEY:
        Window.FileSelector (generateTargetsDB, "Generate DB from")
    elif event == Draw.UKEY:
        Window.FileSelector (linkMaskBug, "Link Mask")
    elif event == Draw.PKEY:
        Window.FileSelector (saveIndexSelectedVerts, "Save index of selected vertices")
    elif event == Draw.AKEY:
        Window.FileSelector (findCloserMesh, "Reconstruct")
    elif event == Draw.JKEY:
        Window.FileSelector (utility6, "adjust foints")









def b_event(event):
    """
    This function handles events when the morph target is being processed.

    Parameters
    ----------

    event:
        *int*. An indicator of the event to be processed

    """
    global symmPath,selAxis,morphFactor
    global current_target
    if event == 0: pass
    elif event == 1:
        Window.FileSelector (saveTranslationTarget, "Save Target",current_target)
    elif event == 2:
        Window.FileSelector (loadTranslationTarget, "Load Target")
    elif event == 3:
        if current_target == "":
            Draw.PupMenu("No target loaded")
        elif current_target > "":
            doMorph(morphFactor.val)
    elif event == 5:
        loadSymVertsIndex(0)
    elif event == 6:
        loadSymVertsIndex(1)
    elif event == 10:
        resetMesh()
    elif event == 20:
        alignMasks()
    Draw.Draw()
Draw.Register(draw, event, b_event)
