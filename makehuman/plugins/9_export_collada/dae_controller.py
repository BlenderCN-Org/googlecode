#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson, Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

Controller export

"""

from .dae_node import rotateLoc, goodBoneName

#----------------------------------------------------------------------
#   library_controllers
#----------------------------------------------------------------------

def writeLibraryControllers(fp, rmeshes, amt, config):
    fp.write('\n  <library_controllers>\n')
    for rmesh in rmeshes:
        writeController(fp, rmesh, amt, config)
    fp.write('  </library_controllers>\n')


def writeController(fp, rmesh, amt, config):
    obj = rmesh.object
    rmesh.calculateSkinWeights(amt)
    nVerts = len(obj.coord)
    nUvVerts = len(obj.texco)
    nFaces = len(obj.fvert)
    nWeights = len(rmesh.skinWeights)
    nBones = len(amt.bones)
    nShapes = len(rmesh.shapes)

    fp.write('\n' +
        '    <controller id="%s-skin">\n' % rmesh.name +
        '      <skin source="#%sMesh">\n' % rmesh.name +
        '        <bind_shape_matrix>\n' +
        '          1 0 0 0 \n' +
        '          0 0 -1 0 \n' +
        '          0 1 0 0 \n' +
        '          0 0 0 1 \n' +
        '        </bind_shape_matrix>\n' +
        '        <source id="%s-skin-joints">\n' % rmesh.name +
        '          <IDREF_array count="%d" id="%s-skin-joints-array">\n' % (nBones,rmesh.name) +
        '           ')

    for bone in amt.bones.values():
        bname = goodBoneName(bone.name)
        fp.write(' %s' % bname)

    fp.write('\n' +
        '          </IDREF_array>\n' +
        '          <technique_common>\n' +
        '            <accessor count="%d" source="#%s-skin-joints-array" stride="1">\n' % (nBones,rmesh.name) +
        '              <param type="IDREF" name="JOINT"></param>\n' +
        '            </accessor>\n' +
        '          </technique_common>\n' +
        '        </source>\n' +
        '        <source id="%s-skin-weights">\n' % rmesh.name +
        '          <float_array count="%d" id="%s-skin-weights-array">\n' % (nWeights,rmesh.name) +
        '           ')

    for w in rmesh.skinWeights:
        fp.write(' %s' % w[1])

    fp.write('\n' +
        '          </float_array>\n' +
        '          <technique_common>\n' +
        '            <accessor count="%d" source="#%s-skin-weights-array" stride="1">\n' % (nWeights,rmesh.name) +
        '              <param type="float" name="WEIGHT"></param>\n' +
        '            </accessor>\n' +
        '          </technique_common>\n' +
        '        </source>\n' +
        '        <source id="%s-skin-poses">\n' % rmesh.name +
        '          <float_array count="%d" id="%s-skin-poses-array">' % (16*nBones,rmesh.name))


    """
    mat = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    for bone in amt.bones.values():
        (x,y,z) = rotateLoc(bone.head, config)
        mat[0][3] = -x
        mat[1][3] = -y
        mat[2][3] = -z
        fp.write('\n            ')
        for i in range(4):
            for j in range(4):
                fp.write('%.4f ' % mat[i][j])

    """

    for bone in amt.bones.values():
        #bone.calcBindMatrix()
        mat = bone.bindMatrix
        mat = bone.getBindMatrixCollada()
        for i in range(4):
            fp.write('\n           ')
            for j in range(4):
                fp.write(' %.4f' % mat[i,j])
        fp.write('\n')

    fp.write('\n' +
        '          </float_array>\n' +
        '          <technique_common>\n' +
        '            <accessor count="%d" source="#%s-skin-poses-array" stride="16">\n' % (nBones,rmesh.name) +
        '              <param type="float4x4"></param>\n' +
        '            </accessor>\n' +
        '          </technique_common>\n' +
        '        </source>\n' +
        '        <joints>\n' +
        '          <input semantic="JOINT" source="#%s-skin-joints"/>\n' % rmesh.name +
        '          <input semantic="INV_BIND_MATRIX" source="#%s-skin-poses"/>\n' % rmesh.name +
        '        </joints>\n' +
        '        <vertex_weights count="%d">\n' % nVerts +
        '          <input offset="0" semantic="JOINT" source="#%s-skin-joints"/>\n' % rmesh.name +
        '          <input offset="1" semantic="WEIGHT" source="#%s-skin-weights"/>\n' % rmesh.name +
        '          <vcount>\n' +
        '            ')

    for wts in rmesh.vertexWeights:
        fp.write('%d ' % len(wts))

    fp.write('\n' +
        '          </vcount>\n'
        '          <v>\n' +
        '           ')

    for wts in rmesh.vertexWeights:
        for pair in wts:
            fp.write(' %d %d' % pair)

    fp.write('\n' +
        '          </v>\n' +
        '        </vertex_weights>\n' +
        '      </skin>\n' +
        '    </controller>\n')

    # Morph controller

    if rmesh.shapes:
        nShapes = len(rmesh.shapes)

        fp.write(
            '    <controller id="%sMorph" name="%sMorph">\n' % (rmesh.name, rmesh.name)+
            '      <morph source="#%sMesh" method="NORMALIZED">\n' % (rmesh.name) +
            '        <source id="%sTargets">\n' % (rmesh.name) +
            '          <IDREF_array id="%sTargets-array" count="%d">' % (rmesh.name, nShapes))

        for key,_ in rmesh.shapes:
            fp.write(" %sMeshMorph_%s" % (rmesh.name, key))

        fp.write(
            '        </IDREF_array>\n' +
            '          <technique_common>\n' +
            '            <accessor source="#%sTargets-array" count="%d" stride="1">\n' % (rmesh.name, nShapes) +
            '              <param name="IDREF" type="IDREF"/>\n' +
            '            </accessor>\n' +
            '          </technique_common>\n' +
            '        </source>\n' +
            '        <source id="%sWeights">\n' % (rmesh.name) +
            '          <float_array id="%sWeights-array" count="%d">' % (rmesh.name, nShapes))

        fp.write(nShapes*" 0")

        fp.write('\n' +
            '        </float_array>\n' +
            '          <technique_common>\n' +
            '            <accessor source="#%sWeights-array" count="%d" stride="1">\n' % (rmesh.name, nShapes) +
            '              <param name="MORPH_WEIGHT" type="float"/>\n' +
            '            </accessor>\n' +
            '          </technique_common>\n' +
            '        </source>\n' +
            '        <targets>\n' +
            '          <input semantic="MORPH_TARGET" source="#%sTargets"/>\n' % (rmesh.name) +
            '          <input semantic="MORPH_WEIGHT" source="#%sWeights"/>\n' % (rmesh.name) +
            '        </targets>\n' +
            '      </morph>\n' +
            '    </controller>\n')


