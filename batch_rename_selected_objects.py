import bpy

for obj in bpy.context.selected_objects:
    name = obj.name.lower()  # 1. 全部小写
    name = name.split('_')[0]  # 2. 删掉第一个下划线及后面内容
    name = name.replace('-', '_')  # 3. - 替换成 _
    name = 'aw_' + name  # 4. 加前缀
    obj.name = name 