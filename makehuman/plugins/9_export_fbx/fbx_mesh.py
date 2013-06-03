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
Fbx mesh
"""

from .fbx_utils import *

#--------------------------------------------------------------------
#   Object definitions
#--------------------------------------------------------------------

def countObjects(stuffs, amt):
    nMeshes = len(stuffs)
    return (nMeshes + 1)


def writeObjectDefs(fp, stuffs, amt, nShapes):
    nMeshes = len(stuffs)

    fp.write(
'    ObjectType: "Geometry" {\n' +
'       Count: %d' % (nMeshes + nShapes) +
"""
        PropertyTemplate: "FbxMesh" {
            Properties70:  {
                P: "Color", "ColorRGB", "Color", "",0.8,0.8,0.8
                P: "BBoxMin", "Vector3D", "Vector", "",0,0,0
                P: "BBoxMax", "Vector3D", "Vector", "",0,0,0
                P: "Primary Visibility", "bool", "", "",1
                P: "Casts Shadows", "bool", "", "",1
                P: "Receive Shadows", "bool", "", "",1
            }
        }
    }
""")

#--------------------------------------------------------------------
#   Object properties
#--------------------------------------------------------------------

def writeObjectProps(fp, stuffs, amt, config):
    for stuff in stuffs:
        name = getStuffName(stuff, amt)
        obj = stuff.meshInfo.object
        writeGeometryProp(fp, name, obj, config)
        writeMeshProp(fp, name, obj)


def writeGeometryProp(fp, name, obj, config):
    id,key = getId("Geometry::%s" % name)
    nVerts = len(obj.coord)
    nFaces = len(obj.fvert)

    fp.write(
'    Geometry: %d, "%s", "Mesh" {\n' % (id, key) +
'        Properties70:  {\n' +
'            P: "MHName", "KString", "", "", "%sMesh"\n' % name +
'        }\n' +
'        Vertices: *%d {\n' % (3*nVerts) +
'            a: ')

    last = nVerts - 1
    for n,co in enumerate(obj.coord):
        fp.write("%.4f,%.4f,%.4f" % (co[0], co[1], co[2]))
        writeComma(fp, n, last)

    last = nFaces - 1
    fp.write(
'        } \n' +
'        PolygonVertexIndex: *%d {\n' % (4*nFaces) +
'            a: ')
    for n,fv in enumerate(obj.fvert):
        if fv[3] == fv[0]:
            fp.write('%d,%d,%d' % (fv[0],fv[1],-1-fv[2]))
        else:
            fp.write('%d,%d,%d,%d' % (fv[0],fv[1],fv[2],-1-fv[3]))
        writeComma(fp, n, last)

    # Must use normals for shapekeys
    obj.calcNormals()
    nNormals = len(obj.vnorm)
    fp.write(
"""
        }
        GeometryVersion: 124
        LayerElementNormal: 0 {
            Version: 101
            Name: ""
            MappingInformationType: "ByPolygonVertex"
            ReferenceInformationType: "IndexToDirect"
""" +
'            Normals: *%d {\n' % (3*nNormals) +
'                a: ')

    last = nNormals - 1
    for n,no in enumerate(obj.vnorm):
        fp.write("%.4f,%.4f,%.4f" % tuple(no))
        writeComma(fp, n, last)
    fp.write(
"""
            }
        }
""")

    writeUvs2(fp, obj)

    fp.write(
"""
        LayerElementMaterial: 0 {
            Version: 101
            Name: "Dummy"
            MappingInformationType: "AllSame"
            ReferenceInformationType: "IndexToDirect"
            Materials: *1 {
                a: 0
            }
        }
        LayerElementTexture: 0 {
            MappingInformationType: "ByPolygonVertex"
            ReferenceInformationType: "IndexToDirect"
            BlendMode: "Translucent"
            Name: "Dummy"
            Version: 101
            TextureAlpha: 1.0
        }
        Layer: 0 {
            Version: 100
            LayerElement:  {
                Type: "LayerElementNormal"
                TypedIndex: 0
            }
            LayerElement:  {
                Type: "LayerElementMaterial"
                TypedIndex: 0
            }
            LayerElement:  {
                Type: "LayerElementTexture"
                TypedIndex: 0
            }
""")
    if config.useNormals:
        fp.write(
"""
            LayerElement:  {
                Type: "LayerElementNormal"
                TypedIndex: 0
            }
""")
    fp.write(
"""
            LayerElement:  {
                Type: "LayerElementUV"
                TypedIndex: 0
            }
        }
    }
""")

#--------------------------------------------------------------------
#   Two different ways to write UVs
#   First method leads to crash in AD FBX converter
#--------------------------------------------------------------------

def writeUvs1(fp, obj):
    nUvVerts = len(obj.texco)
    nUvFaces = len(obj.fuvs)

    fp.write(
"""
        LayerElementUV: 0 {
            Version: 101
            Name: ""
            MappingInformationType: "ByPolygonVertex"
            ReferenceInformationType: "IndexToDirect"
""")

    fp.write(
'            UV: *%d {\n' % (2*nUvVerts) +
'                a: ')

    last = nUvVerts - 1
    for n,uv in enumerate(obj.texco):
        fp.write("%.4f,%.4f" % (uv[0], uv[1]))
        writeComma(fp, n, last)

    fp.write(
'            } \n'
'            UVIndex: *%d {\n' % (4*nUvFaces) +
'                a: ')

    last = nUvFaces - 1
    for n,fuv in enumerate(obj.fuvs):
        if fuv[3] == fuv[0]:
            fp.write('%d,%d,%d' % (fuv[0],fuv[1],fuv[2]))
        else:
            fp.write('%d,%d,%d,%d' % (fuv[0],fuv[1],fuv[2],fuv[3]))
        writeComma(fp, n, last)
    fp.write(
"""
            }
        }
""")


def writeUvs2(fp, obj):
    nUvVerts = len(obj.texco)
    nUvFaces = len(obj.fuvs)

    fp.write(
"""
        LayerElementUV: 0 {
            Version: 101
            Name: ""
            MappingInformationType: "ByPolygonVertex"
            ReferenceInformationType: "IndexToDirect"
""")
    fp.write(
'            UV: *%d {\n' % (8*nUvFaces) +
'                a: ')

    last = 4*nUvFaces - 1
    n = 0
    for fuv in obj.fuvs:
        for vt in fuv:
            uv = obj.texco[vt]
            fp.write('%.4f,%.4f' % (uv[0], uv[1]))
            writeComma(fp, n, last)
            n += 1

    fp.write(
'            } \n'
'            UVIndex: *%d {\n' % (4*nUvFaces) +
'                a: ')

    last = nUvFaces - 1
    for n,fuv in enumerate(obj.fuvs):
        fp.write('%d,%d,%d,%d' % (4*n,4*n+1,4*n+2,4*n+3))
        writeComma(fp, n, last)

    fp.write(
"""
            }
        }
""")


#--------------------------------------------------------------------
#
#--------------------------------------------------------------------

def writeMeshProp(fp, name, obj):
    id,key = getId("Model::%sMesh" % name)
    fp.write(
'    Model: %d, "%s", "Mesh" {' % (id, key) +
"""
        Version: 232
        Properties70:  {
            P: "RotationActive", "bool", "", "",1
            P: "InheritType", "enum", "", "",1
            P: "ScalingMax", "Vector3D", "Vector", "",0,0,0
            P: "DefaultAttributeIndex", "int", "Integer", "",0
""" +
'            P: "MHName", "KString", "", "", "%s"' % name +
"""
        }
        Shading: Y
        Culling: "CullingOff"
    }
""")

#--------------------------------------------------------------------
#   Links
#--------------------------------------------------------------------

def writeLinks(fp, stuffs, amt):
    for stuff in stuffs:
        name = getStuffName(stuff, amt)
        ooLink(fp, 'Model::%sMesh' % name, 'Model::RootNode')
        if amt:
            ooLink(fp, 'Model::%sMesh' % name, 'Model::%s' % amt.name)
        ooLink(fp, 'Geometry::%s' % name, 'Model::%sMesh' % name)


