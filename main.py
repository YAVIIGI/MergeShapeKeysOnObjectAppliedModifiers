import bpy

def setActiveObject(objectName):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[objectName].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[objectName]
    
sklist = []
oName = bpy.context.selected_objects[0].name

for s in bpy.context.selected_objects[0].data.shape_keys.key_blocks.keys():
    sklist.append(s)
    
for sk in sklist:

    # set active to original Object
    setActiveObject(oName)

    # copy and rename
    bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":(0,0,0)})

    # set self shape key
    if sk != 'Basis':
        # rename partial shape object
        bpy.data.objects[oName + '.001'].name = sk

        # set shape key value to 1
        bpy.data.objects[sk].data.shape_keys.key_blocks[sk].value = 1

        # convert to MESH
        bpy.ops.object.convert(target='MESH')

        # join shape
        setActiveObject(oName + '-base')
        bpy.data.objects[sk].select_set(True)
        bpy.ops.object.join_shapes()

        # delete partial shape object
        setActiveObject(sk)
        bpy.ops.object.delete(use_global=False, confirm=False)

    else:

        # rename base object
        bpy.data.objects[oName + ".001"].name = oName + '-base'

        # convert to MESH
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.shape_key_add(from_mix=False)
    
setActiveObject(oName + '-base')