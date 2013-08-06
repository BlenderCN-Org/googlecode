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

Material export

"""

import os

#----------------------------------------------------------------------
#   library_images
#----------------------------------------------------------------------

def writeLibraryImages(fp, rmeshes, config):
    fp.write('\n  <library_images>\n')
    for rmesh in rmeshes:
        writeImages(fp, rmesh, config)
    fp.write('  </library_images>\n')


def writeImages(fp, rmesh, config):
    mat = rmesh.material
    if mat.diffuseTexture:
        writeImage(fp, mat.diffuseTexture, config)
    if mat.specularMapTexture:
        writeImage(fp, mat.specularMapTexture, config)
    if mat.bumpMapTexture:
        writeImage(fp, mat.bumpMapTexture, config)
    if mat.normalMapTexture:
        writeImage(fp, mat.normalMapTexture, config)
    if mat.displacementMapTexture:
        writeImage(fp, mat.displacementMapTexture, config)


def getTextureName(filepath):
    texfile = os.path.basename(filepath)
    return texfile.replace(".","_")


def writeImage(fp, filepath, config):
    if not filepath:
        return
    newpath = config.copyTextureToNewLocation(filepath)
    print "Collada Image", filepath, newpath
    texname = getTextureName(filepath)
    fp.write(
        '    <image id="%s" name="%s">\n' % (texname, texname) +
        '      <init_from>%s</init_from>\n' % newpath +
        '    </image>\n'
    )

#----------------------------------------------------------------------
#   library_effects
#----------------------------------------------------------------------

def writeLibraryEffects(fp, rmeshes, config):
    fp.write('\n  <library_effects>\n')
    for rmesh in rmeshes:
        writeEffects(fp, rmesh)
    fp.write('  </library_effects>\n')


def writeEffects(fp, rmesh):
    mat = rmesh.material
    fp.write(
       '    <effect id="%s-effect">\n' % mat.name.replace(" ", "_") +
       '      <profile_COMMON>\n')

    writeSurfaceSampler(fp, mat.diffuseTexture)
    writeSurfaceSampler(fp, mat.specularMapTexture)
    writeSurfaceSampler(fp, mat.normalMapTexture)
    writeSurfaceSampler(fp, mat.bumpMapTexture)
    writeSurfaceSampler(fp, mat.displacementMapTexture)

    fp.write(
        '        <technique sid="common">\n' +
        '          <phong>\n')

    writeTexture(fp, 'diffuse', mat.diffuseTexture, mat.diffuseColor, mat.diffuseIntensity)
    writeTexture(fp, 'transparency', mat.diffuseTexture, None, mat.transparencyIntensity)
    writeTexture(fp, 'specular', mat.specularMapTexture, mat.specularColor, 0.1*mat.specularIntensity)
    writeIntensity(fp, 'shininess', mat.specularHardness)
    writeTexture(fp, 'normal', mat.normalMapTexture, None, mat.normalMapIntensity)
    writeTexture(fp, 'bump', mat.bumpMapTexture, None, mat.bumpMapIntensity)
    writeTexture(fp, 'displacement', mat.displacementMapTexture, None, mat.displacementMapIntensity)

    fp.write(
        '          </phong>\n' +
        '          <extra/>\n' +
        '        </technique>\n' +
        '        <extra>\n' +
        '          <technique profile="GOOGLEEARTH">\n' +
        '            <show_double_sided>1</show_double_sided>\n' +
        '          </technique>\n' +
        '        </extra>\n' +
        '      </profile_COMMON>\n' +
        '      <extra><technique profile="MAX3D"><double_sided>1</double_sided></technique></extra>\n' +
        '    </effect>\n')


def writeSurfaceSampler(fp, filepath):
    if not filepath:
        return
    texname = getTextureName(filepath)
    fp.write(
        '        <newparam sid="%s-surface">\n' % texname +
        '          <surface type="2D">\n' +
        '            <init_from>%s</init_from>\n' % texname +
        '          </surface>\n' +
        '        </newparam>\n' +
        '        <newparam sid="%s-sampler">\n' % texname +
        '          <sampler2D>\n' +
        '            <source>%s-surface</source>\n' % texname +
        '          </sampler2D>\n' +
        '        </newparam>\n')

def writeIntensity(fp, tech, intensity):
    fp.write('            <%s><float>%s</float></%s>\n' % (tech, intensity, tech))


def writeTexture(fp, tech, filepath, color, intensity, s=1.0):
    if not filepath:
        return

    fp.write('            <%s>\n' % tech)
    if color:
        fp.write('            <color>%.4f %.4f %.4f 1</color> \n' % (s*color.r, s*color.g, s*color.b))
    if intensity:
        fp.write('            <float>%s</float>\n' % intensity)
    texname = getTextureName(filepath)
    fp.write(
        '              <texture texture="%s-sampler" texcoord="UVTex"/>\n' % texname +
        '            </%s>\n' % tech)

#----------------------------------------------------------------------
#   library_materials
#----------------------------------------------------------------------

def writeLibraryMaterials(fp, rmeshes, config):
    fp.write('\n  <library_materials>\n')
    for rmesh in rmeshes:
        writeMaterials(fp, rmesh)
    fp.write('  </library_materials>\n')


def writeMaterials(fp, rmesh):
    mat = rmesh.material
    matname = mat.name.replace(" ", "_")
    fp.write(
        '    <material id="%s" name="%s">\n' % (matname, matname) +
        '      <instance_effect url="#%s-effect"/>\n' % matname +
        '    </material>\n')

