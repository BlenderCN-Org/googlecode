"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         GPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
Vertex groups

"""

import bpy

#
#    removeVertexGroups(context):
#    class VIEW3D_OT_RemoveVertexGroupsButton(bpy.types.Operator):
#

def removeVertexGroups(context):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.vertex_group_remove(all=True)
    return

class VIEW3D_OT_RemoveVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhw.remove_vertex_groups"
    bl_label = "Unvertex all"
    bl_options = {'UNDO'}

    def execute(self, context):
        removeVertexGroups(context)
        print("All vertex groups removed")
        return{'FINISHED'}

#
#
#

class VIEW3D_OT_IntegerVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhw.integer_vertex_groups"
    bl_label = "Integer vertex groups"
    bl_options = {'UNDO'}

    def execute(self, context):
        ob = context.object
        for v in ob.data.vertices:
            wmax = -1
            best = None
            for g in v.groups:
                if g.weight > wmax:
                    wmax = g.weight
                    best = g.group
            if not best:
                continue
            for g in v.groups:
                if g.group == best:
                    g.weight = 1
                else:
                    g.weight = 0
        print("Integer vertex groups done")
        return{'FINISHED'}

#
#
#

def copyVertexGroups(scn, src, trg):
    print("Copy vertex groups %s => %s" % (src.name, trg.name))
    scn.objects.active = trg
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.vertex_group_remove(all=True)
    groups = {}
    for sgrp in src.vertex_groups:
        tgrp = trg.vertex_groups.new(name=sgrp.name)
        groups[sgrp.index] = tgrp
    for vs in src.data.vertices:
        for g in vs.groups:
            tgrp = groups[g.group]
            tgrp.add([vs.index], g.weight, 'REPLACE')
    return

class VIEW3D_OT_CopyVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhw.copy_vertex_groups"
    bl_label = "Copy vgroups active => selected"
    bl_options = {'UNDO'}

    def execute(self, context):
        src = context.object
        scn = context.scene
        for ob in scn.objects:
            if ob.type == 'MESH' and ob != src:
                trg = ob
                break
        copyVertexGroups(scn, src, trg)
        print("Vertex groups copied")
        return{'FINISHED'}

#
#
#

def mergeVertexGroups(scn, ob):
    vgroups = []
    for n in range(5):
        vg = scn["MhxVG%d" % n]
        if vg:
            vgroups.append(vg)
        else:
            break
    if not vgroups:
        return
    print("Merging", vgroups)
    tgrp = ob.vertex_groups[vgroups[0]]
    groups = []
    for vg in vgroups:
        groups.append( ob.vertex_groups[vg].index )
    for v in ob.data.vertices:
        w = 0
        for g in v.groups:
            if g.group in groups:
                w += g.weight
        if w > 1e-4:
            tgrp.add([v.index], w, 'REPLACE')
    for vgname in vgroups[1:]:
        vg = ob.vertex_groups[vgname]
        print("Remove", vg)
        ob.vertex_groups.remove(vg)
    return

class VIEW3D_OT_MergeVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhw.merge_vertex_groups"
    bl_label = "Merge vertex groups"
    bl_options = {'UNDO'}

    def execute(self, context):
        mergeVertexGroups(context.scene, context.object)
        print("Vertex groups merged")
        return{'FINISHED'}


#
#    unVertexDiamonds(context):
#    class VIEW3D_OT_UnvertexDiamondsButton(bpy.types.Operator):
#

def unVertexDiamonds(context):
    ob = context.object
    print("Unvertex diamonds in %s" % ob)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    me = ob.data
    for f in me.polygons:
        if len(f.vertices) < 4:
            for vn in f.vertices:
                me.vertices[vn].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.vertex_group_remove_from(all=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    return

class VIEW3D_OT_UnvertexDiamondsButton(bpy.types.Operator):
    bl_idname = "mhw.unvertex_diamonds"
    bl_label = "Unvertex diamonds"
    bl_options = {'UNDO'}

    def execute(self, context):
        unVertexDiamonds(context)
        print("Diamonds unvertexed")
        return{'FINISHED'}

class VIEW3D_OT_UnvertexSelectedButton(bpy.types.Operator):
    bl_idname = "mhw.unvertex_selected"
    bl_label = "Unvertex selected"
    bl_options = {'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.vertex_group_remove_from(all=True)
        bpy.ops.object.mode_set(mode='OBJECT')
        print("Selected unvertexed")
        return{'FINISHED'}

#
#
#

class VIEW3D_OT_MultiplyWeightsButton(bpy.types.Operator):
    bl_idname = "mhw.multiply_weights"
    bl_label = "Multiply weights"
    bl_options = {'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.wm.context_set_value(data_path="tool_settings.mesh_select_mode", value="(True,False,False)")
        bpy.ops.object.mode_set(mode='OBJECT')
        ob = context.object
        factor = context.scene.MhxWeight
        index = ob.vertex_groups.active_index
        for v in ob.data.vertices:
            if v.select:
                print(v, index)
                for g in v.groups:
                    if g.group == index:
                        g.weight *= factor
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.wm.context_set_value(data_path="tool_settings.mesh_select_mode", value="(False,True,False)")
        print("Weights multiplied")
        return{'FINISHED'}

#
#    deleteDiamonds(context)
#    Delete joint diamonds in main mesh
#    class VIEW3D_OT_DeleteDiamondsButton(bpy.types.Operator):
#

def deleteDiamonds(context):
    ob = context.object
    print("Delete diamonds in %s" % bpy.context.object)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    me = ob.data
    for f in me.polygons:
        if len(f.vertices) < 4:
            for vn in f.vertices:
                me.vertices[vn].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    return

class VIEW3D_OT_DeleteDiamondsButton(bpy.types.Operator):
    bl_idname = "mhw.delete_diamonds"
    bl_label = "Delete diamonds"
    bl_options = {'UNDO'}

    def execute(self, context):
        deleteDiamonds(context)
        print("Diamonds deleted")
        return{'FINISHED'}


#
#    pairWeight(context):
#

def findGroupPairs(context):
    ob = context.object
    scn = context.scene
    name1 = scn['MhxBone1']
    name2 = scn['MhxBone2']
    weight = scn['MhxWeight']
    group1 = None
    group2 = None
    for vgrp in ob.vertex_groups:
        if vgrp.name == name1:
            group1 = vgrp
        if vgrp.name == name2:
            group2 = vgrp
    if not (group1 and group2):
        raise NameError("Did not find vertex groups %s or %s" % (name1, name2))
    return (group1, group2)


def pairWeight(context):
    ob = context.object
    (group1, group2) = findGroupPairs(context)
    index1 = group1.index
    index2 = group2.index
    for v in ob.data.vertices:
        if v.select:
            for grp in v.groups:
                if grp.index == index1:
                    grp.weight = weight
                elif grp.index == index2:
                    grp.weight = 1-weight
                else:
                    ob.remove_from_group(grp, v.index)
    return


class VIEW3D_OT_PairWeightButton(bpy.types.Operator):
    bl_idname = "mhw.pair_weight"
    bl_label = "Weight pair"
    bl_options = {'UNDO'}

    def execute(self, context):
        pairWeight(context)
        return{'FINISHED'}


def rampWeight(context):
    ob = context.object
    (group1, group2) = findGroupPairs(context)
    xmin = 1e6
    xmax = -1e6
    for v in ob.data.vertices:
        if v.select:
            x = v.co[0]
            if x < xmin: xmin = x
            if x > xmax: xmax = x
    factor = 1/(xmax-xmin)
    for v in ob.data.vertices:
        if v.select:
            x = v.co[0]
            w = factor*(x-xmin)
            group1.add([v.index], 1-w, 'REPLACE')
            group2.add([v.index], w, 'REPLACE')
    return


class VIEW3D_OT_RampWeightButton(bpy.types.Operator):
    bl_idname = "mhw.ramp_weight"
    bl_label = "Weight ramp"
    bl_options = {'UNDO'}

    def execute(self, context):
        rampWeight(context)
        return{'FINISHED'}


def createLeftRightGroups(context):
    ob = context.object
    left = ob.vertex_groups.new(name="Left")
    right = ob.vertex_groups.new(name="Right")
    xmax = 0.1
    factor = 1/(2*xmax)
    for v in ob.data.vertices:
        w = factor*(v.co[0]+xmax)
        if w > 1:
            left.add([v.index], 1, 'REPLACE')
        elif w < 0:
            right.add([v.index], 1, 'REPLACE')
        else:
            left.add([v.index], w, 'REPLACE')
            right.add([v.index], 1-w, 'REPLACE')
    return


class VIEW3D_OT_CreateLeftRightButton(bpy.types.Operator):
    bl_idname = "mhw.create_left_right"
    bl_label = "Create Left Right"
    bl_options = {'UNDO'}

    def execute(self, context):
        createLeftRightGroups(context)
        return{'FINISHED'}

