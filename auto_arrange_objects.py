bl_info = {
    "name": "Auto Arrange Objects",
    "author": "AI Assistant",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object > Context Menu",
    "description": "自动将选中物体按方形网格平铺分布（适应不同尺寸）",
    "category": "Object",
}

import bpy
from mathutils import Vector
import math

class OBJECT_OT_auto_arrange(bpy.types.Operator):
    bl_idname = "object.auto_arrange"
    bl_label = "自动排列（方形平铺）"
    bl_options = {'REGISTER', 'UNDO'}

    gap: bpy.props.FloatProperty(
        name="间距",
        default=0.2,
        min=0.0,
        description="物体之间的最小间隔"
    )

    def execute(self, context):
        objs = context.selected_objects
        objs = sorted(objs, key=lambda o: o.name)
        count = len(objs)
        if count == 0:
            self.report({'WARNING'}, "未选中任何物体")
            return {'CANCELLED'}
        cols = math.ceil(math.sqrt(count))
        rows = math.ceil(count / cols)
        widths = []
        heights = []
        for i in range(cols):
            col_objs = objs[i::cols]
            max_width = 0
            for obj in col_objs:
                bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
                min_x = min([v.x for v in bbox])
                max_x = max([v.x for v in bbox])
                width = max_x - min_x
                if width > max_width:
                    max_width = width
            widths.append(max_width)
        for j in range(rows):
            row_objs = objs[j*cols:(j+1)*cols]
            max_height = 0
            for obj in row_objs:
                bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
                min_y = min([v.y for v in bbox])
                max_y = max([v.y for v in bbox])
                height = max_y - min_y
                if height > max_height:
                    max_height = height
            heights.append(max_height)
        start_x = 0
        start_y = 0
        for idx, obj in enumerate(objs):
            row = idx // cols
            col = idx % cols
            bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
            min_x = min([v.x for v in bbox])
            max_x = max([v.x for v in bbox])
            min_y = min([v.y for v in bbox])
            max_y = max([v.y for v in bbox])
            width = max_x - min_x
            height = max_y - min_y
            x = start_x + sum(widths[:col]) + col * self.gap + width / 2
            y = start_y + sum(heights[:row]) + row * self.gap + height / 2
            obj.location.x = x
            obj.location.y = y
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_auto_arrange.bl_idname, icon='GRID')

def register():
    bpy.utils.register_class(OBJECT_OT_auto_arrange)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_auto_arrange)

if __name__ == "__main__":
    register()
