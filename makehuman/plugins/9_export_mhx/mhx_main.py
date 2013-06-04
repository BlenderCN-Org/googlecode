#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makeinfo.human.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makeinfo.human.org/node/318)

**Coding Standards:**  See http://www.makeinfo.human.org/node/165

Abstract
--------

MakeHuman to MHX (MakeHuman eXchange format) exporter. MHX files can be loaded into Blender
"""

MAJOR_VERSION = 1
MINOR_VERSION = 15
BODY_LANGUAGE = True

import module3d
import gui3d
import os
import time
import numpy
import math
import log

#import cProfile

import mh2proxy
import exportutils
import warpmodifier
import posemode
import exportutils

from . import posebone
from . import mhx_materials
from . import mhx_mesh
from . import mhx_proxy
from . import mhx_armature
from . import mhx_pose


class MhxEnvironment:
    def __init__(self, amt, config, proxies):
        self.armature = amt
        self.config = config
        self.proxies = proxies

#-------------------------------------------------------------------------------
#   Export MHX file
#-------------------------------------------------------------------------------

def exportMhx(human, filepath, config):
    gui3d.app.progress(0, text="Exporting MHX")
    log.message("Exporting %s" % filepath.encode('utf-8'))
    time1 = time.clock()
    posemode.exitPoseMode()
    posemode.enterPoseMode()

    config.setHuman(human)
    config.setupTexFolder(filepath)

    filename = os.path.basename(filepath)
    name = config.goodName(os.path.splitext(filename)[0])
    amt = mhx_armature.getArmature(name, human, config.rigOptions)
    fp = open(filepath, 'w')
    fp.write(
        "# MakeHuman exported MHX\n" +
        "# www.makeinfo.human.org\n" +
        "MHX %d %d ;\n" % (MAJOR_VERSION, MINOR_VERSION) +
        "#if Blender24\n" +
        "  error 'This file can only be read with Blender 2.5' ;\n" +
        "#endif\n")

    proxies = scanProxies(human, config)
    env = MhxEnvironment(amt, config, proxies)
    amt.setup()

    if not config.cage:
        fp.write(
            "#if toggle&T_Cage\n" +
            "  error 'This MHX file does not contain a cage. Unselect the Cage import option.' ;\n" +
            "#endif\n")

    fp.write("NoScale True ;\n")
    amt.setupCustomShapes(fp)

    gui3d.app.progress(0.1, text="Exporting armature")
    amt.writeArmature(fp, MINOR_VERSION, proxies)

    gui3d.app.progress(0.15, text="Exporting materials")
    fp.write("\nNoScale False ;\n\n")
    mhx_materials.writeMaterials(fp, env)

    if config.cage:
        mhx_proxy.writeProxyType('Cage', 'T_Cage', env, fp, 0.2, 0.25)

    gui3d.app.progress(0.25, text="Exporting main mesh")
    fp.write("#if toggle&T_Mesh\n")
    mhx_mesh.writeMesh(fp, human.meshData, env)
    fp.write("#endif\n")

    mhx_proxy.writeProxyType('Proxy', 'T_Proxy', env, fp, 0.35, 0.4)
    mhx_proxy.writeProxyType('Clothes', 'T_Clothes', env, fp, 0.4, 0.55)
    mhx_proxy.writeProxyType('Hair', 'T_Clothes', env, fp, 0.55, 0.6)

    mhx_pose.writePose(fp, env)

    writeGroups(fp, env)

    if amt.options.rigtype == 'rigify':
        fp.write("Rigify %s ;\n" % amt.name)

    fp.close()
    log.message("%s exported" % filepath.encode('utf-8'))
    gui3d.app.progress(1.0)
    return

#-------------------------------------------------------------------------------
#   Scan proxies
#-------------------------------------------------------------------------------

def scanProxies(human, config):
    proxies = {}
    for pfile in config.getProxyList():
        if pfile.file:
            proxy = mh2proxy.readProxyFile(human.meshData, pfile, True)
            if proxy:
                proxies[proxy.name] = proxy
    return proxies

#-------------------------------------------------------------------------------
#   Groups
#-------------------------------------------------------------------------------

def writeGroups(fp, env):
    amt = env.armature
    fp.write("""
# ---------------- Groups -------------------------------- #

""")
    fp.write(
        "PostProcess %sMesh %s 0000003f 00080000 %s 0000c000 ;\n" % (amt.name, amt.name, amt.boneLayers) +
        "Group %s\n"  % amt.name +
        "  Objects\n" +
        "    ob %s ;\n" % amt.name +
        "#if toggle&T_Mesh\n" +
        "    ob %sMesh ;\n" % amt.name +
        "#endif\n")

    groupProxy('Cage', 'T_Cage', fp, env)
    groupProxy('Proxy', 'T_Proxy', fp, env)
    groupProxy('Clothes', 'T_Clothes', fp, env)
    groupProxy('Hair', 'T_Clothes', fp, env)

    fp.write(
        "    ob CustomShapes ;\n" +
        "  end Objects\n" +
        "  layers Array 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  ;\n" +
        "end Group\n")
    return


def groupProxy(typ, test, fp, env):
    amt = env.armature
    fp.write("#if toggle&%s\n" % test)
    for proxy in env.proxies.values():
        if proxy.type == typ:
            name = amt.name + proxy.name
            fp.write("    ob %sMesh ;\n" % name)
    fp.write("#endif\n")
    return

