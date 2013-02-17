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
Exports proxy mesh to obj

"""

import os
import exportutils
import mh2proxy

#
#    exportProxyObj(human, filepath, config):    
#

def exportProxyObj(human, filepath, config):
    obj = human.meshData
    config.addObjects(human)
    config.setupTexFolder(filepath)
    filename = os.path.basename(filepath)
    name = config.goodName(os.path.splitext(filename)[0])

    stuffs = exportutils.collect.setupObjects(
        name, 
        human,
        config=config,
        helpers=config.helpers, 
        hidden=config.hidden, 
        eyebrows=config.eyebrows, 
        lashes=config.lashes,
        subdivide=config.subdivide)
    
    fp = open(filepath, 'w')
    fp.write(
"# MakeHuman exported OBJ\n" +
"# www.makehuman.org\n\n" +
"mtllib %s.mtl\n" % os.path.basename(filepath))
    for stuff in stuffs:
        writeGeometry(fp, stuff)
    fp.close()
    
    mtlfile = "%s.mtl" % filepath
    fp = open(mtlfile, 'w')
    fp.write(
'# MakeHuman exported MTL\n' +
'# www.makehuman.org\n\n')
    for stuff in stuffs:
        writeMaterial(fp, stuff, human, config)
    fp.close()
    return

#
#    writeGeometry(fp, stuff):
#
        
def writeGeometry(fp, stuff):
    obj = stuff.meshInfo.object
    nVerts = len(obj.verts)
    nUvVerts = len(obj.texco)
    fp.write("usemtl %s\n" % stuff.name)
    fp.write("g %s\n" % stuff.name)    
    for co in obj.coord:
        fp.write("v %.4g %.4g %.4g\n" % tuple(co))
    for v in obj.verts:
        fp.write("vn %.4g %.4g %.4g\n" % tuple(v.no))
    if 0 and obj.has_uv:
        for uv in obj.texco:
            fp.write("vt %.4g %.4g\n" % tuple(uv))
        for f in obj.faces:
            fp.write('f ')
            for n,v in enumerate(f.verts):
                uv = f.uv[n]
                fp.write("%d/%d " % (v.idx-nVerts, uv-nUvVerts))
            fp.write('\n')
    else:            
        for f in obj.faces:
            fp.write('f ')
            for v in f.verts:
                fp.write("%d " % (v.idx-nVerts))
            fp.write('\n')
    return        

#
#   writeMaterial(fp, stuff, human, config):
#

def writeMaterial(fp, stuff, human, config):
    fp.write("\nnewmtl %s\n" % stuff.name)
    diffuse = (1, 1, 1)
    spec = (1, 1, 1)
    diffScale = 0.8
    specScale = 0.02
    alpha = 1
    if stuff.material:
        for (key, value) in stuff.material.settings:
            if key == "diffuse_color":
                diffuse = value
            elif key == "specular_color":
                spec = value
            elif key == "diffuse_intensity":
                diffScale = value
            elif key == "specular_intensity":
                specScale = value
            elif key == "alpha":
                alpha = value
                
    fp.write(
    "Kd %.4g %.4g %.4g\n" % (diffScale*diffuse[0], diffScale*diffuse[1], diffScale*diffuse[2]) +
    "Ks %.4g %.4g %.4g\n" % (specScale*spec[0], specScale*spec[1], specScale*spec[2]) +
    "d %.4g\n" % alpha
    )
    
    if stuff.proxy:
        writeTexture(fp, "map_Kd", stuff.texture, human, config)
        #writeTexture(fp, "map_Tr", stuff.proxy.translucency, human, config)
        writeTexture(fp, "map_Disp", stuff.proxy.normal, human, config)
        writeTexture(fp, "map_Disp", stuff.proxy.displacement, human, config)
    else:        
        writeTexture(fp, "map_Kd", ("data/textures", "texture.png"), human, config)


def writeTexture(fp, key, texture, human, config):
    if not texture:
        return
    (folder, texfile) = texture
    texpath = config.getTexturePath(texfile, folder, True, human)        
    (fname, ext) = os.path.splitext(texfile)  
    name = "%s_%s" % (fname, ext[1:])
    print(texpath)
    fp.write("%s %s\n" % (key, texpath))
    

"""    
Ka 1.0 1.0 1.0
Kd 1.0 1.0 1.0
Ks 0.33 0.33 0.52
illum 5
Ns 50.0
map_Kd texture.png
"""
