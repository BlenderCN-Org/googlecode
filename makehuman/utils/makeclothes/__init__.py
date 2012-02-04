""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
Utility for making clothes to MH characters.

For more info see: http://sites.google.com/site/makehumandocs/blender-export-and-mhx/making-clothes

"""
bl_info = {
    "name": "Make Clothes",
    "author": "Thomas Larsson",
    "version": "0.6",
    "blender": (2, 6, 1),
    "api": 40000,
    "location": "View3D > Properties > Make MH clothes",
    "description": "Make clothes for MakeHuman characters",
    "warning": "",
    'wiki_url': '',
    "category": "MakeHuman"}


if "bpy" in locals():
    print("Reloading makeclothes")
    import imp
    imp.reload(main)
    imp.reload(base_uv)
else:
    print("Loading makeclothes")
    import bpy
    import os
    from bpy.props import *
    from . import main
    from . import base_uv
  
#
#    class MakeClothesPanel(bpy.types.Panel):
#

class MakeClothesPanel(bpy.types.Panel):
    bl_label = "Make clothes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'MESH')

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.label("Initialization")
        if not main.isInited(scn):
            layout.operator("mhclo.init_interface", text="Initialize")
            return
        layout.operator("mhclo.init_interface", text="ReInitialize")
        layout.operator("mhclo.factory_settings")
        layout.operator("mhclo.save_settings")

        layout.label("Utilities")
        layout.operator("mhclo.print_vnums")
        layout.operator("mhclo.remove_vertex_groups")
        layout.operator("mhclo.auto_vertex_groups")
        layout.operator("mhclo.copy_vert_locs")
        
        layout.label("Settings")
        layout.prop(scn, "MCDirectory")
        layout.prop(scn, "MCMaterials")
        layout.prop(scn, "MCBlenderMaterials")
        layout.prop(scn, "MCHairMaterial")
        layout.label("Set mesh type")
        row = layout.row()
        row.operator("mhclo.make_human", text="Human").isHuman = True
        row.operator("mhclo.make_human", text="Clothing").isHuman = False
        
        layout.label("UV layers")
        row = layout.row()
        row.prop(scn, "MCMaskLayer", text="Mask")   
        row.prop(scn, "MCTextureLayer", text = "Texture")   
        row.prop(scn, "MCObjLayer", text="Obj")   

        layout.separator()
        layout.label("Make clothes")
        layout.operator("mhclo.make_clothes")
        layout.separator()
        layout.operator("mhclo.export_obj_file")
        layout.operator("mhclo.export_blender_material")
        
        layout.label("UVs")
        layout.operator("mhclo.recover_seams")
        layout.operator("mhclo.project_uvs")
        layout.operator("mhclo.reexport_mhclo")        
        
        layout.label("Shapekeys")
        for skey in main.ShapeKeys:
            layout.prop(scn, "MC%s" % skey)   
        
        layout.label("Z depth")
        layout.prop(scn, "MCZDepthName")   
        layout.operator("mhclo.set_zdepth")
        layout.prop(scn, "MCZDepth")   

        layout.label("Boundary")
        layout.prop(scn, "MCBodyPart")   
        layout.prop(scn, "MCExamineBoundary")           
        layout.operator("mhclo.set_boundary")        
        row = layout.row()
        row.prop(scn, "MCX1")
        row.prop(scn, "MCX2")
        row = layout.row()
        row.prop(scn, "MCY1")
        row.prop(scn, "MCY2")
        row = layout.row()
        row.prop(scn, "MCZ1")
        row.prop(scn, "MCZ2")   
        if not main.UseInternal:
            return

        layout.separator()
        layout.label("For internal use")
        layout.prop(scn, "MCListLength")
        layout.prop(scn, "MCLogging")
        layout.prop(scn, "MCSelfClothed")
        layout.prop(scn, "MCMakeHumanDirectory")
        layout.operator("mhclo.split_human")
        layout.operator("mhclo.export_base_uvs_py")

        #layout.prop(scn, "MCVertexGroups")
        #layout.operator("mhclo.offset_clothes")
        return

#
#    class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
#

class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
    bl_idname = "mhclo.init_interface"
    bl_label = "Init"

    def execute(self, context):
        main.initInterface(context.scene)
        main.readDefaultSettings(context)
        print("Interface initialized")
        return{'FINISHED'}    

#
#    class OBJECT_OT_FactorySettingsButton(bpy.types.Operator):
#

class OBJECT_OT_FactorySettingsButton(bpy.types.Operator):
    bl_idname = "mhclo.factory_settings"
    bl_label = "Restore factory settings"

    def execute(self, context):
        main.initInterface(context.scene)
        return{'FINISHED'}    

#
#    class OBJECT_OT_SaveSettingsButton(bpy.types.Operator):
#

class OBJECT_OT_SaveSettingsButton(bpy.types.Operator):
    bl_idname = "mhclo.save_settings"
    bl_label = "Save settings"

    def execute(self, context):
        main.saveDefaultSettings(context)
        return{'FINISHED'}    

#
#    class OBJECT_OT_RecoverSeamsButton(bpy.types.Operator):
#

class OBJECT_OT_RecoverSeamsButton(bpy.types.Operator):
    bl_idname = "mhclo.recover_seams"
    bl_label = "Recover seams"

    def execute(self, context):
        main.recoverSeams(context)
        return{'FINISHED'}    

#
#    class OBJECT_OT_MakeClothesButton(bpy.types.Operator):
#

class OBJECT_OT_MakeClothesButton(bpy.types.Operator):
    bl_idname = "mhclo.make_clothes"
    bl_label = "Make clothes"

    def execute(self, context):     
        main.makeClothes(context)
        return{'FINISHED'}    
        
#
#    class OBJECT_OT_ProjectUVsButton(bpy.types.Operator):
#

class OBJECT_OT_ProjectUVsButton(bpy.types.Operator):
    bl_idname = "mhclo.project_uvs"
    bl_label = "Project UVs"

    def execute(self, context):
        (human, clothing) = main.getObjectPair(context)
        main.unwrapObject(clothing, context)
        main.projectUVs(human, clothing, context)
        return{'FINISHED'}    
        
#
#   class OBJECT_OT_CopyVertLocsButton(bpy.types.Operator):
#

class OBJECT_OT_CopyVertLocsButton(bpy.types.Operator):
    bl_idname = "mhclo.copy_vert_locs"
    bl_label = "Copy vertex locations"

    def execute(self, context):
        src = context.object
        for trg in context.scene.objects:
            if trg != src and trg.select and trg.type == 'MESH':
                print("Copy vertex locations from %s to %s" % (src.name, trg.name))
                for n,sv in enumerate(src.data.vertices):
                    tv = trg.data.vertices[n]
                    tv.co = sv.co
                print("Vertex locations copied")
        return{'FINISHED'}    

        
#
#   class OBJECT_OT_ExportObjFileButton(bpy.types.Operator):
#

class OBJECT_OT_ExportObjFileButton(bpy.types.Operator):
    bl_idname = "mhclo.export_obj_file"
    bl_label = "Export Obj file"

    def execute(self, context):
        main.exportObjFile(context)
        return{'FINISHED'}    

#
#   class OBJECT_OT_ReexportMhcloButton(bpy.types.Operator):
#

class OBJECT_OT_ReexportMhcloButton(bpy.types.Operator):
    bl_idname = "mhclo.reexport_mhclo"
    bl_label = "Reexport Mhclo file"

    def execute(self, context):
        main.reexportMhclo(context)
        return{'FINISHED'}    

#
#   class OBJECT_OT_ExportBaseUvsPyButton(bpy.types.Operator):
#   class OBJECT_OT_SplitHumanButton(bpy.types.Operator):
#

class OBJECT_OT_ExportBaseUvsPyButton(bpy.types.Operator):
    bl_idname = "mhclo.export_base_uvs_py"
    bl_label = "Export base UV py file"

    def execute(self, context):
        main.exportBaseUvsPy(context)
        return{'FINISHED'}    
        
class OBJECT_OT_SplitHumanButton(bpy.types.Operator):
    bl_idname = "mhclo.split_human"
    bl_label = "Split human"

    def execute(self, context):
        main.getObjectPair(context)
        return{'FINISHED'}    
                
#
#    class OBJECT_OT_ExportBlenderMaterialsButton(bpy.types.Operator):
#

class OBJECT_OT_ExportBlenderMaterialButton(bpy.types.Operator):
    bl_idname = "mhclo.export_blender_material"
    bl_label = "Export Blender material"

    def execute(self, context):
        pob = main.getClothing(context)
        (outpath, outfile) = main.getFileName(pob, context, "mhx")
        main.exportBlenderMaterial(pob.data, outpath)
        return{'FINISHED'}    

#
#    class OBJECT_OT_MakeHumanButton(bpy.types.Operator):
#

class OBJECT_OT_MakeHumanButton(bpy.types.Operator):
    bl_idname = "mhclo.make_human"
    bl_label = "Make human"
    isHuman = BoolProperty()

    def execute(self, context):
        ob = context.object
        ob["MhxMesh"] = self.isHuman
        print("Object %s: Human = %s" % (ob.name, ob["MhxMesh"]))
        return{'FINISHED'}    

#
#    class OBJECT_OT_SetBoundaryButton(bpy.types.Operator):
#

class OBJECT_OT_SetBoundaryButton(bpy.types.Operator):
    bl_idname = "mhclo.set_boundary"
    bl_label = "Set boundary"

    def execute(self, context):
        main.setBoundary(context)        
        return{'FINISHED'}    

#
#    class OBJECT_OT_OffsetClothesButton(bpy.types.Operator):
#

class OBJECT_OT_OffsetClothesButton(bpy.types.Operator):
    bl_idname = "mhclo.offset_clothes"
    bl_label = "Offset clothes"

    def execute(self, context):     
        main.offsetCloth(context)
        return{'FINISHED'}    

#
#    class OBJECT_OT_SetZDepthButton(bpy.types.Operator):
#

class OBJECT_OT_SetZDepthButton(bpy.types.Operator):
    bl_idname = "mhclo.set_zdepth"
    bl_label = "Set Z depth"

    def execute(self, context):
        main.setZDepth(context.scene)
        return{'FINISHED'}    
   
#
#    class VIEW3D_OT_MhxPrintVnumsButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxPrintVnumsButton(bpy.types.Operator):
    bl_idname = "mhclo.print_vnums"
    bl_label = "Print vertex numbers"

    def execute(self, context):
        main.printVertNums(context)
        return{'FINISHED'}    

#
#    class VIEW3D_OT_MhxRemoveVertexGroupsButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxRemoveVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhclo.remove_vertex_groups"
    bl_label = "Remove vertex groups"

    def execute(self, context):
        main.removeVertexGroups(context)
        print("All vertex groups removed")
        return{'FINISHED'}    

#
#   class VIEW3D_OT_MhxAutoVertexGroupsButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxAutoVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhclo.auto_vertex_groups"
    bl_label = "Auto vertex groups"

    def execute(self, context):
        main.removeVertexGroups(context)
        main.autoVertexGroups(context)
        print("Vertex groups auto assigned")
        return{'FINISHED'}    


#
#    Init and register
#

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

