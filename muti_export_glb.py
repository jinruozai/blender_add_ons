bl_info = {
    "name": "batch_export_glb",
    "author": "AI Assistant",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > N面板 > 批量GLB导出",
    "description": "在N面板批量导出选中物体为独立GLB文件",
    "category": "Object",
}

import bpy
import os
from bpy.props import StringProperty, BoolProperty, EnumProperty

class BatchGLBExporterProperties(bpy.types.PropertyGroup):
    export_dir: StringProperty(
        name="导出目录",
        description="选择导出文件夹",
        subtype='DIR_PATH',
        default=""
    )
    export_format: EnumProperty(
        name="格式",
        items=[
            ('GLB', 'glTF Binary (.glb)', ''),
            ('GLTF_EMBEDDED', 'glTF Embedded (.gltf)', ''),
            ('GLTF_SEPARATE', 'glTF Separate (.gltf + .bin + textures)', ''),
        ],
        default='GLB'
    )
    export_apply: BoolProperty(
        name="Apply Modifiers",
        default=True
    )
    export_yup: BoolProperty(
        name="+Y Up",
        default=True
    )

class OBJECT_OT_batch_export_glb(bpy.types.Operator):
    bl_idname = "object.batch_export_glb"
    bl_label = "批量导出GLB"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.batch_glb_exporter
        export_dir = props.export_dir
        if not export_dir:
            self.report({'WARNING'}, "请先选择导出目录！")
            return {'CANCELLED'}
        selected_objs = context.selected_objects
        if not selected_objs:
            self.report({'WARNING'}, "未选中任何物体！")
            return {'CANCELLED'}
        for obj in selected_objs:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            export_path = os.path.join(export_dir, obj.name + ".glb")
            bpy.ops.export_scene.gltf(
                filepath=export_path,
                use_selection=True,
                export_format=props.export_format,
                export_apply=props.export_apply,
                export_yup=props.export_yup
            )
        self.report({'INFO'}, f"已导出 {len(selected_objs)} 个GLB文件到: {export_dir}")
        return {'FINISHED'}

class VIEW3D_PT_batch_glb_exporter(bpy.types.Panel):
    bl_label = "批量GLB导出"
    bl_idname = "VIEW3D_PT_batch_glb_exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "批量GLB导出"

    def draw(self, context):
        layout = self.layout
        props = context.scene.batch_glb_exporter
        layout.prop(props, "export_dir")
        layout.prop(props, "export_format")
        layout.prop(props, "export_apply")
        layout.prop(props, "export_yup")
        layout.operator("object.batch_export_glb", icon='EXPORT')

classes = [
    BatchGLBExporterProperties,
    OBJECT_OT_batch_export_glb,
    VIEW3D_PT_batch_glb_exporter
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.batch_glb_exporter = bpy.props.PointerProperty(type=BatchGLBExporterProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.batch_glb_exporter

if __name__ == "__main__":
    register()
