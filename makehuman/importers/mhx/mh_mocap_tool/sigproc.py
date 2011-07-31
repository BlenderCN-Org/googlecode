#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Project Name:        MakeHuman
# Product Home Page:   http://www.makehuman.org/
# Code Home Page:      http://code.google.com/p/makehuman/
# Authors:             Thomas Larsson
# Script copyright (C) MakeHuman Team 2001-2011
# Coding Standards:    See http://sites.google.com/site/makehumandocs/developers-guide

import bpy
from bpy.props import StringProperty, FloatProperty, IntProperty, BoolProperty, EnumProperty
from . import simplify, load
from . import globvar as the


#
#   class CFilterData:
#

class CFilterData:
    def __init__(self):
        self.object = ""
        self.Gs = {}
        self.Ls = {}
        self.fb = 0
        self.m = 0

the.filterData = {}

#
#   calcFilters(context):
#

def calcFilters(context):
    rig = context.object
    (fcurves, minTime, maxTime) = simplify.getRigFCurves(rig, False, False)
    if not fcurves:
        return            

    try:
        fd = the.filterData[rig.name]
    except:
        fd = CFilterData()
        the.filterData[rig.name] = fd
    fd.Gs = {}
    fd.Ls = {}

    tmin = 100000
    tmax = -100000
    for fcu in fcurves:
        (points, before, after) = simplify.splitFCurvePoints(fcu, minTime, maxTime)
        pt0 = points[0]
        ptn = points[-1]
        t0 = int(pt0.co[0])
        tn = int(ptn.co[0]) 
        if t0 < tmin: tmin = t0
        if tn > tmax: tmax = tn

    m = tmax - tmin + 1
    m1 = m
    fb = 0
    while m1 > 1:
        fb += 1
        m1 = m1 >> 1
    fd.m = m    
    fd.fb = fb

    a = 3/8
    b = 1/4
    c = 1/16
    for fcu in fcurves:
        Gk = {}
        for n in range(m):
            Gk[n] = fcu.evaluate(n + t0)
        print(fcu.data_path)
        G = {}
        G[0] = Gk
        p = 1
        for k in range(fb):
            Gl = {}
            if 2*p >= m-2*p:
                print("Bug %d %d" % (m,p))
            for n in range(0,m):
                np = n+p
                n2p = n+2*p
                nq = n-p
                n2q = n-2*p
                if np >= m: np = m-1                    
                if n2p >= m: n2p = m-1                    
                if nq < 0: nq = 0
                if n2q < 0: n2q = 0
                Gl[n] = a*Gk[n] + b*(Gk[nq] + Gk[np]) + c*(Gk[n2q] + Gk[n2p])
            p *= 2
            Gk = Gl
            G[k+1] = Gl

        L = {}
        Gl = G[0]
        for k in range(fb):
            Lk = {} 
            Gk = Gl
            Gl = G[k+1]
            for n in range(m):
                Lk[n] = Gk[n] - Gl[n]
            L[k] = Lk

        key = "%s_%d" % (fcu.data_path, fcu.array_index)
        fd.Gs[key] = G
        fd.Ls[key] = L

    for k in range(fb-1):
        rig["s_%d" % k] = 1.0
    return

#
#   reconstructFCurves(context):
#

def reconstructFCurves(context):
    rig = context.object
    fd = the.filterData[rig.name]
    s = {}
    for k in range(fd.fb-1):
        s[k] = rig["s_%d" % k]
    print(fd.fb, fd.m)

    (fcurves, minTime, maxTime) = simplify.getRigFCurves(rig, False, False)
    act = rig.animation_data.action
    nact = bpy.data.actions.new(act.name)
    
    for fcu in fcurves:
        path = fcu.data_path
        index = fcu.array_index
        grp = fcu.group.name
        key = "%s_%d" % (path, index)
        G = fd.Gs[key]
        L = fd.Ls[key]

        print(path)
        Gk = G[fd.fb]
        x = {}
        for n in range(fd.m):
            x[n] = Gk[n]
        for k in range(fd.fb-1):
            sk = s[k]
            Lk = L[k]    
            for n in range(fd.m):
                x[n] += sk*Lk[n]

        nfcu = nact.fcurves.new(path, index, grp)
        for n in range(fd.m):
            nfcu.keyframe_points.insert(frame=n, value=x[n])

    rig.animation_data.action = nact
    load.setInterpolation(rig)
    return


########################################################################
#
#   class VIEW3D_OT_CalcFiltersButton(bpy.types.Operator):
#

class VIEW3D_OT_CalcFiltersButton(bpy.types.Operator):
    bl_idname = "mcp.calc_filters"
    bl_label = "Calc filters"

    def execute(self, context):
        calcFilters(context)
        print("Filters calculated")
        return{'FINISHED'}    

#
#   class VIEW3D_OT_ReconstructFCurvesButton(bpy.types.Operator):
#

class VIEW3D_OT_ReconstructFCurvesButton(bpy.types.Operator):
    bl_idname = "mcp.reconstruct_fcurves"
    bl_label = "Reconstruct F-curves"

    def execute(self, context):
        reconstructFCurves(context)
        print("F-curves reconstructed")
        return{'FINISHED'}    

#
#    class PlantPanel(bpy.types.Panel):
#

class SigProcPanel(bpy.types.Panel):
    bl_label = "Motion signal processing"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        if context.object and context.object.type == 'ARMATURE':
            return True

    def draw(self, context):
        layout = self.layout
        ob = context.object
        layout.operator("mcp.calc_filters")
        try:
            fd = the.filterData[ob.name]
        except:
            fd = None
        if fd:
            layout.operator("mcp.reconstruct_fcurves")
            for k in range(fd.fb-1):
                layout.prop(ob, '["s_%d"]' % k)

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

