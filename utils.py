import bpy
import math
import mathutils

# Constants
TRANSFORM_ITEMS = [
    ('ROT_X', "Rotation X", "Use X axis rotation"),
    ('ROT_Y', "Rotation Y", "Use Y axis rotation"),
    ('ROT_Z', "Rotation Z", "Use Z axis rotation"),
    ('LOC_X', "Location X", "Use X axis location"),
    ('LOC_Y', "Location Y", "Use Y axis location"),
    ('LOC_Z', "Location Z", "Use Z axis location"),
    ('SCALE_X', "Scale X", "Use X axis scale"),
    ('SCALE_Y', "Scale Y", "Use Y axis scale"),
    ('SCALE_Z', "Scale Z", "Use Z axis scale"),
]

def ensure_template_collection():
    """Ensure template collection exists and create if missing"""
    template_collection = None
    for collection in bpy.context.scene.collection.children:
        if collection.name == "ShapeKeySliderTemplates":
            template_collection = collection
            break
            
    if template_collection is None:
        template_collection = bpy.data.collections.new("ShapeKeySliderTemplates")
        bpy.context.scene.collection.children.link(template_collection)
        template_collection.hide_viewport = True
        template_collection.hide_render = True
    
    return template_collection

def create_templates(template_collection):
    """Create required template objects for shape key controls"""
    # Create slider line template
    if "slider_line_template" not in template_collection.objects:
        bpy.ops.mesh.primitive_plane_add(size=1)
        slider_line = bpy.context.view_layer.objects.active
        slider_line.name = "slider_line_template"
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.object.mode_set(mode='OBJECT')
        for col in slider_line.users_collection:
            col.objects.unlink(slider_line)
        template_collection.objects.link(slider_line)

    if "slider_handle_template" not in template_collection.objects:
        bpy.ops.mesh.primitive_circle_add(radius=0.1, vertices=16)
        handle = bpy.context.view_layer.objects.active
        handle.name = "slider_handle_template"
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.edge_face_add()
        bpy.ops.object.mode_set(mode='OBJECT')
        for col in handle.users_collection:
            col.objects.unlink(handle)
        template_collection.objects.link(handle)

def setup_shape_key_driver(armature, bone_name, shape_key, transform_type, multiplier=30.0):
    """Set up driver for shape key control
    
    Args:
        armature: Armature object containing the control bone
        bone_name: Name of the control bone
        shape_key: Shape key to be controlled
        transform_type: Type of transform to use (LOC/ROT/SCALE)
        multiplier: Driver influence multiplier
    """
    try:
        # 기존 드라이버 제거
        if shape_key.id_data.animation_data:
            for driver in shape_key.id_data.animation_data.drivers:
                if driver.data_path == f'key_blocks["{shape_key.name}"].value':
                    shape_key.id_data.animation_data.drivers.remove(driver)
        
        # 새 드라이버 추가
        driver = shape_key.driver_add('value').driver
        driver.type = 'SCRIPTED'
        var = driver.variables.new()
        var.name = "bone_transform"
        var.type = 'TRANSFORMS'
        
        # 타겟 설정
        target = var.targets[0]
        target.id = armature
        target.bone_target = bone_name
        target.transform_type = transform_type
        target.transform_space = 'LOCAL_SPACE'
        
        # 드라이버 표현식 설정
        if 'ROT' in transform_type:
            driver.expression = f"bone_transform * {57.2958 * multiplier}"  # 라디안을 도로 변환하고 multiplier 적용
        elif 'LOC' in transform_type:
            driver.expression = f"bone_transform * {multiplier}"
        else:  # SCALE
            driver.expression = f"(bone_transform - 1.0) * {multiplier}"
        
        # 드라이버 설정 후 Basis 쉐이프키 선택
        mesh_obj = None
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj.data.shape_keys == shape_key.id_data:
                mesh_obj = obj
                break
                
        if mesh_obj:
            mesh_obj.active_shape_key_index = 0  # Basis 선택
        
        return True, ""
        
    except Exception as e:
        return False, str(e)
    
def get_available_meshes(context):
    """Returns visible mesh objects with shape keys"""
    meshes = [obj for obj in context.scene.objects 
             if (obj.type == 'MESH' and 
                 obj.visible_get() and
                 obj.data.shape_keys)]
    return meshes

def draw_shape_key_list(layout, mesh_obj):
    """Draw shape key list UI"""
    shape_keys = mesh_obj.data.shape_keys
    
    for key_block in shape_keys.key_blocks[1:]:
        row = layout.row(align=True)
        value_row = row.split(factor=0.7, align=True)
        value_row.prop(key_block, "value", text=key_block.name)
        
        if shape_keys.animation_data and shape_keys.animation_data.drivers:
            for driver in shape_keys.animation_data.drivers:
                if driver.data_path == f'key_blocks["{key_block.name}"].value':
                    var = driver.driver.variables[0]
                    transform_type = var.targets[0].transform_type
                    current_value = get_driver_value(driver, transform_type)
                    
                    # UI 처리
                    sub_row = value_row.row(align=True)
                    if isinstance(current_value, str):  # 문자열인 경우
                        if current_value == "Custom":
                            sub_row.label(text="Custom", icon='DRIVER')
                        else:
                            # 수식을 표시
                            sub_row.label(text=current_value, icon='DRIVER')
                    else:
                        # 숫자값인 경우 기존 UI 사용
                        props = sub_row.operator("shape.adjust_driver_value", 
                                              text=f"{current_value:.1f}", 
                                              icon='DRIVER')
                        props.mesh_name = mesh_obj.name
                        props.shape_key_name = key_block.name
                        props.transform_type = transform_type
                        props.value = current_value
                    break

def get_driver_value(driver, transform_type):
    """Calculate current value of driver"""
    try:
        expression = driver.driver.expression
        
        # 애드온으로 만든 표준 형식 체크
        if 'bone_transform' in expression:
            if 'ROT' in transform_type:
                return float(expression.split('*')[2]) / 57.2958
            elif 'LOC' in transform_type:
                return float(expression.split('*')[1])
            else:  # SCALE
                return float(expression.split('*')[1])
        
        # 사용자 정의 드라이버 처리
        else:
            # 복잡한 수식인 경우 원본 표시
            if any(op in expression for op in ['+', '-', '*', '/', '(', ')']):
                return expression  # 수식 그대로 반환
            
            # 단순 숫자만 있는 경우
            try:
                return float(expression)
            except:
                return "Custom"  # 파싱 불가능한 경우
            
    except Exception as e:
        print(f"Error parsing driver value: {e}")
        return "Custom"

def update_driver_expression(driver, value, transform_type, mesh_obj=None):
    """
    Update driver expression
    Args:
        driver: Driver object
        value: New value
        transform_type: Transform type
        mesh_obj: Mesh object (optional)
    """
    rounded_value = round(value, 1)
    
    if 'ROT' in transform_type:
        driver.expression = f"bone_transform * {57.2958 * rounded_value:.1f}"
    elif 'LOC' in transform_type:
        driver.expression = f"bone_transform * {rounded_value}"
    else:  # SCALE
        driver.expression = f"(bone_transform - 1.0) * {rounded_value}"
    
    # 메쉬 객체가 제공된 경우 Basis 선택
    if mesh_obj:
        mesh_obj.active_shape_key_index = 0
        
def calculate_widget_transforms(bone_matrix, bone_length, shape_key=None):
    """Calculate widget transforms based on bone and shape key
    
    Args:
        bone_matrix: World matrix of the bone
        bone_length: Length of the bone
        shape_key: Optional shape key for offset calculation
    
    Returns:
        dict: Dictionary containing transform information
    """
    bone_loc = bone_matrix.translation
    bone_rot = bone_matrix.to_euler('XYZ')
    bone_rot_quat = bone_matrix.to_quaternion()
    
    # 기본 스케일과 오프셋 설정
    base_scale = bone_length * 0.5
    slider_width = bone_length * 2
    slider_height = bone_length * 0.1
    text_scale = bone_length * 0.4
    
    # 슬라이더 오프셋 계산
    base_offset = mathutils.Vector((-slider_width / 2, 0, 0))
    
    # 쉐이프 키 범위에 따른 오프셋 조정
    if shape_key:
        min_value = shape_key.slider_min
        max_value = shape_key.slider_max
        
        if min_value == -1 and max_value == 1:
            base_offset = mathutils.Vector((0, 0, 0))
        elif not (min_value == 0 and max_value == 1):
            total_range = max_value - min_value
            mid_value = (max_value + min_value) / 2
            offset_ratio = -mid_value / total_range
            x_offset = slider_width * offset_ratio
            base_offset += mathutils.Vector((x_offset, 0, 0))
    
    # 오프셋을 본의 회전에 맞춰 회전
    base_offset.rotate(bone_rot_quat)
    
    # 텍스트 오프셋 계산
    text_offset = mathutils.Vector((0, bone_length * 0.3, 0))
    text_offset.rotate(bone_rot_quat)
    
    return {
        "bone_loc": bone_loc,
        "bone_rot": bone_rot,
        "bone_rot_quat": bone_rot_quat,
        "base_scale": base_scale,
        "slider_width": slider_width,
        "slider_height": slider_height,
        "text_scale": text_scale,
        "base_offset": base_offset,
        "text_offset": text_offset
    }

def apply_widget_transforms(obj, transforms, obj_type):
    """Apply calculated transforms to widget object
    
    Args:
        obj: Widget object to transform
        transforms: Dictionary of transform information
        obj_type: Type of widget ('TEXT', 'SLIDE', or 'WGT')
    """
    if obj_type == 'TEXT':
        obj.location = transforms["bone_loc"] + transforms["text_offset"]
        obj.rotation_euler = transforms["bone_rot"]
        obj.scale = mathutils.Vector((transforms["text_scale"],) * 3)
        
    elif obj_type == 'SLIDE':
        obj.location = transforms["bone_loc"] - transforms["base_offset"]
        obj.rotation_mode = 'XYZ'
        obj.rotation_euler = (math.radians(90), 
                            transforms["bone_rot"].y, 
                            transforms["bone_rot"].z)
        obj.scale = mathutils.Vector((transforms["slider_width"], 
                                    transforms["slider_height"], 
                                    transforms["base_scale"]))
        
    elif obj_type == 'WGT':
        obj.location = transforms["bone_loc"]
        obj.rotation_euler = transforms["bone_rot"]
        obj.scale = mathutils.Vector((transforms["base_scale"],) * 3)

def setup_bone_constraints(pose_bone, transform_type):
    """Set up bone constraints for shape key control
    
    Args:
        pose_bone: Pose bone to set up constraints on
        transform_type: Type of transform to limit
    """
    # 기존 제약 조건 제거
    for const in pose_bone.constraints:
        pose_bone.constraints.remove(const)

    if 'LOC' in transform_type:
        const = pose_bone.constraints.new('LIMIT_LOCATION')
        const.name = "Shape Key Control"
        const.owner_space = 'LOCAL'  # 로컬 스페이스로 설정
        const.use_transform_limit = True  # 변환 제한 활성화
        
        # 축 제한 설정
        const.use_min_x = True
        const.use_max_x = True
        const.use_min_y = True
        const.use_max_y = True
        const.use_min_z = True
        const.use_max_z = True
        
        if 'X' in transform_type:
            const.min_x = -1.0
            const.max_x = 1.0
            const.use_min_y = False
            const.use_max_y = False
            const.use_min_z = False
            const.use_max_z = False
        elif 'Y' in transform_type:
            const.min_y = -1.0
            const.max_y = 1.0
            const.use_min_x = False
            const.use_max_x = False
            const.use_min_z = False
            const.use_max_z = False
        elif 'Z' in transform_type:
            const.min_z = -1.0
            const.max_z = 1.0
            const.use_min_x = False
            const.use_max_x = False
            const.use_min_y = False
            const.use_max_y = False

    elif 'ROT' in transform_type:
        const = pose_bone.constraints.new('LIMIT_ROTATION')
        const.name = "Shape Key Control"
        const.owner_space = 'LOCAL'
        const.use_transform_limit = True
        
        const.use_limit_x = True
        const.use_limit_y = True
        const.use_limit_z = True
        
        if 'X' in transform_type:
            const.min_x = -1.571
            const.max_x = 1.571
            const.use_limit_y = False
            const.use_limit_z = False
        elif 'Y' in transform_type:
            const.min_y = -1.571
            const.max_y = 1.571
            const.use_limit_x = False
            const.use_limit_z = False
        elif 'Z' in transform_type:
            const.min_z = -1.571
            const.max_z = 1.571
            const.use_limit_x = False
            const.use_limit_y = False

    elif 'SCALE' in transform_type:
        const = pose_bone.constraints.new('LIMIT_SCALE')
        const.name = "Shape Key Control"
        const.owner_space = 'LOCAL'
        const.use_transform_limit = True
        
        const.use_min_x = True
        const.use_max_x = True
        const.use_min_y = True
        const.use_max_y = True
        const.use_min_z = True
        const.use_max_z = True
        
        if 'X' in transform_type:
            const.min_x = 0.0
            const.max_x = 2.0
            const.use_min_y = False
            const.use_max_y = False
            const.use_min_z = False
            const.use_max_z = False
        elif 'Y' in transform_type:
            const.min_y = 0.0
            const.max_y = 2.0
            const.use_min_x = False
            const.use_max_x = False
            const.use_min_z = False
            const.use_max_z = False
        elif 'Z' in transform_type:
            const.min_z = 0.0
            const.max_z = 2.0
            const.use_min_x = False
            const.use_max_x = False
            const.use_min_y = False
            const.use_max_y = False

    # 본의 변환 모드 설정
    pose_bone.rotation_mode = 'XYZ'
    
def create_shape_key_text_widget(context, text_name, text_body, bone=None, shape_key=None):
    """Create text widget for shape key control
    
    Args:
        context: Current context
        text_name: Name for the text object
        text_body: Content of the text
        bone: Optional pose bone to attach widget to
    """
    try:
        # 현재 선택된 오브젝트와 모드 저장
        active_object = context.active_object
        active_mode = context.mode
        
        # 오브젝트 모드로 전환
        if active_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            
        # 본의 월드 매트릭스 계산
        if bone and isinstance(bone, bpy.types.PoseBone):
            armature = active_object
            world_matrix = armature.matrix_world @ bone.matrix
            bone_loc = world_matrix.translation
            bone_rot = world_matrix.to_euler('XYZ')
            # 본의 길이 계산
            bone_length = bone.length
            # 본 길이를 기준으로 기본 스케일 설정
            base_scale = bone_length * 0.5  # 본 길이의 절반을 기본 크기로
            slider_width = bone_length * 2  # 슬라이더 길이는 본 길이의 2배
            slider_height = bone_length * 0.1  # 슬라이더 높이는 본 길이의 10%
            text_scale = bone_length * 0.4  # 텍스트 크기는 본 길이의 40%
        else:
            bone_loc = mathutils.Vector((0, 0, 0))
            bone_rot = mathutils.Euler((0, 0, 0))
            base_scale = 0.2
            slider_width = base_scale * 4
            slider_height = base_scale * 0.2
            text_scale = base_scale

        # 템플릿 컬렉션 확인 및 생성
        template_collection = ensure_template_collection()
        create_templates(template_collection)

        # 슬라이더 라인 복제
        line_template = template_collection.objects.get("slider_line_template")
        if not line_template:
            return None, "Slider line template not found!"
            
        slider_line = line_template.copy()
        slider_line.name = f"SLIDE_{text_name}"
        slider_line.data = line_template.data.copy()

        # 핸들 복제
        handle_template = template_collection.objects.get("slider_handle_template")
        if not handle_template:
            return None, "Slider handle template not found!"
            
        handle = handle_template.copy()
        handle.name = text_name
        handle.data = handle_template.data.copy()

        # 텍스트 생성
        bpy.ops.object.text_add(location=bone_loc)
        text_obj = context.active_object
        text_obj.name = f"TEXT_{text_name}"
        text_obj.data.body = text_body
        text_obj.data.align_x = 'CENTER'
        text_obj.data.fill_mode = 'NONE'

        # 본의 회전 정보 계산
        bone_rot_quat = world_matrix.to_quaternion()

        # 위치 및 크기 조정
        handle.location = bone_loc
        handle.rotation_euler = bone_rot
        handle.scale = mathutils.Vector((base_scale, base_scale, base_scale))

        # 슬라이더 오프셋 계산
        base_offset = mathutils.Vector((-slider_width / 2, 0, 0))  # 기본 위치

        # shape_key가 ShapeKey 객체인 경우 범위 확인
        if shape_key and isinstance(shape_key, bpy.types.ShapeKey):
            min_value = shape_key.slider_min
            max_value = shape_key.slider_max
            
            print(f"Shape key range: {min_value} ~ {max_value}")
            
            if min_value == -1 and max_value == 1:
                # -1~1 범위일 경우 본이 중앙에 오도록
                base_offset = mathutils.Vector((0, 0, 0))
                print("Centered slider")
            elif not (min_value == 0 and max_value == 1):
                # 다른 범위의 경우 기존 계산 유지
                total_range = max_value - min_value
                mid_value = (max_value + min_value) / 2
                offset_ratio = -mid_value / total_range
                x_offset = slider_width * offset_ratio
                base_offset += mathutils.Vector((x_offset, 0, 0))
                print(f"Offset slider by {x_offset}")

        # 오프셋을 본의 회전에 맞춰 회전
        base_offset.rotate(bone_rot_quat)

        # 슬라이더 설정
        slider_line.location = bone_loc - base_offset
        slider_line.rotation_mode = 'XYZ'
        slider_line.rotation_euler = (math.radians(90), bone_rot.y, bone_rot.z)
        slider_line.scale = mathutils.Vector((slider_width, slider_height, base_scale))

        # 텍스트 위치 조정
        text_offset = mathutils.Vector((0, bone_length * 0.3, 0))  # 본 길이의 30% 만큼 위로
        text_offset.rotate(bone_rot_quat)
        text_obj.location = bone_loc + text_offset
        text_obj.rotation_euler = bone_rot
        text_obj.scale = mathutils.Vector((text_scale, text_scale, text_scale))

        # 모든 오브젝트를 와이어프레임으로 표시
        text_obj.display_type = 'WIRE'
        slider_line.display_type = 'WIRE'
        handle.display_type = 'WIRE'

        # Widgets 컬렉션 확인 또는 생성
        widgets_collection = bpy.data.collections.get("Widgets")
        if not widgets_collection:
            widgets_collection = bpy.data.collections.new("Widgets")
            context.scene.collection.children.link(widgets_collection)

        # 위젯 세트를 위한 새 컬렉션 생성
        widget_set_collection = bpy.data.collections.new(text_name)
        widgets_collection.children.link(widget_set_collection)

        # 현재 컬렉션에서 제거하고 새 위젯 세트 컬렉션으로 이동
        for obj in [text_obj, slider_line, handle]:
            if obj.name in context.scene.collection.objects:
                context.scene.collection.objects.unlink(obj)
            for col in obj.users_collection:
                col.objects.unlink(obj)
            widget_set_collection.objects.link(obj)

        # 본이 제공된 경우 커스텀 쉐이프로 설정
        if bone and isinstance(bone, bpy.types.PoseBone):
            bone.custom_shape = handle
            bone.use_custom_shape_bone_size = True
            bone.custom_shape_scale_xyz = (1, 1, 1)
            bone.custom_shape_translation = (0, 0, 0)
            bone.custom_shape_rotation_euler = (0, 0, 0)

        # 원래 모드로 복원
        if active_mode != 'OBJECT':
            context.view_layer.objects.active = active_object
            bpy.ops.object.mode_set(mode=active_mode)

        return handle, ""

    except Exception as e:
        print(f"Error in create_shape_key_text_widget: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, str(e)
    
def get_meshes_with_drivers(self, context):
    """드라이버가 있는 메쉬 목록 생성"""
    items = []
    
    # 본 이름 가져오기
    if context.mode == 'EDIT_ARMATURE':
        bone_name = context.active_bone.name
    else:  # POSE
        bone_name = context.active_pose_bone.name
    
    # 드라이버가 있는 메쉬 검색
    for obj in context.scene.objects:
        if obj.type == 'MESH' and obj.data.shape_keys and obj.data.shape_keys.animation_data:
            has_driver = False
            for driver in obj.data.shape_keys.animation_data.drivers:
                for var in driver.driver.variables:
                    if (var.type == 'TRANSFORMS' and 
                        var.targets[0].bone_target == bone_name):
                        has_driver = True
                        break
                if has_driver:
                    items.append((obj.name, obj.name, ""))
                    break
    
    return items

def get_shape_key_drivers(self, context):
    """선택된 메쉬의 모든 쉐이프 키 드라이버 목록 생성"""
    items = []
    
    if not hasattr(self, 'target_mesh') or not self.target_mesh:
        return items

    # 선택된 메쉬의 드라이버 검사
    obj = bpy.data.objects.get(self.target_mesh)
    if obj and obj.data.shape_keys and obj.data.shape_keys.animation_data:
        shape_keys = obj.data.shape_keys
        
        # 모든 드라이버 순회
        for driver in shape_keys.animation_data.drivers:
            # 쉐이프 키 이름 추출
            try:
                # 드라이버 데이터 경로에서 쉐이프 키 이름 추출
                # 예: 'key_blocks["name"].value' -> 'name'
                shape_key_name = driver.data_path.split('"')[1]
                items.append((shape_key_name, shape_key_name, ""))
            except:
                continue
    
    return items

def store_custom_widgets(armature):
    """Store custom widget information for bones
    Only stores custom widgets that start with 'WGT_shape_key_ctrl'
    """
    stored_widgets = {}
    for pose_bone in armature.pose.bones:
        if (pose_bone.custom_shape and 
            pose_bone.custom_shape.name.startswith('WGT_shape_key_ctrl')):
            stored_widgets[pose_bone.name] = {
                'widget': pose_bone.custom_shape,
                'size': pose_bone.use_custom_shape_bone_size,
                'scale': pose_bone.custom_shape_scale_xyz,
                'translation': pose_bone.custom_shape_translation,
                'rotation': pose_bone.custom_shape_rotation_euler
            }
    return stored_widgets

def restore_custom_widgets(armature, stored_widgets):
    """Restore custom widget information to bones"""
    for bone_name, widget_info in stored_widgets.items():
        if bone_name in armature.pose.bones:
            pose_bone = armature.pose.bones[bone_name]
            # 위젯이 여전히 존재하는지 확인
            if widget_info['widget'] and widget_info['widget'].name in bpy.data.objects:
                pose_bone.custom_shape = widget_info['widget']
                pose_bone.use_custom_shape_bone_size = widget_info['size']
                pose_bone.custom_shape_scale_xyz = widget_info['scale']
                pose_bone.custom_shape_translation = widget_info['translation']
                pose_bone.custom_shape_rotation_euler = widget_info['rotation']

def transform_handler(scene):
    """Transform handler for auto-sync"""
    try:
        if (scene.is_sync_enabled and 
            scene.metarig and 
            scene.rigify_rig and 
            bpy.context.mode == 'EDIT_ARMATURE' and
            bpy.context.active_bone and
            bpy.context.active_object == scene.rigify_rig):
            
            # 현재 본 정보
            rigify_bone = bpy.context.active_bone
            bone_name = rigify_bone.name
            
            # 연결된 위젯 찾기
            widget_name = f"WGT_{bone_name}"
            widget_collection = None
            widget_objects = []
            
            # 모든 컬렉션에서 위젯 검색
            for collection in bpy.data.collections:
                for obj in collection.objects:
                    if obj.name.startswith(widget_name):
                        widget_collection = collection
                        widget_objects = [obj for obj in collection.objects 
                                        if obj.name.startswith(('WGT_', 'SLIDE_', 'TEXT_'))]
                        break
                if widget_collection:
                    break
            
            # 위젯이 있는 경우 위치 업데이트
            if widget_objects:
                # 쉐이프 키 찾기
                shape_key = None
                for obj in widget_objects:
                    if obj.name.startswith('WGT_'):
                        # 위젯 이름에서 본 이름 추출
                        widget_bone_name = obj.name[4:]  # 'WGT_' 제외
                        # 연결된 메쉬에서 쉐이프 키 찾기
                        for mesh_obj in bpy.data.objects:
                            if (mesh_obj.type == 'MESH' and 
                                mesh_obj.data.shape_keys and 
                                mesh_obj.data.shape_keys.animation_data):
                                for driver in mesh_obj.data.shape_keys.animation_data.drivers:
                                    if widget_bone_name in driver.data_path:
                                        shape_key_name = driver.data_path.split('"')[1]
                                        shape_key = mesh_obj.data.shape_keys.key_blocks[shape_key_name]
                                        break
                                if shape_key:
                                    break
                        break
                
                # 본 매트릭스 계산
                bone_matrix = scene.metarig.matrix_world @ scene.metarig.pose.bones[bone_name].matrix
                
                # 트랜스폼 계산 및 적용
                transforms = calculate_widget_transforms(
                    bone_matrix,
                    scene.metarig.pose.bones[bone_name].length,
                    shape_key
                )
                
                # 각 위젯 오브젝트 업데이트
                for obj in widget_objects:
                    if obj.name.startswith('WGT_'):
                        apply_widget_transforms(obj, transforms, 'WGT')
                    elif obj.name.startswith('SLIDE_'):
                        apply_widget_transforms(obj, transforms, 'SLIDE')
                    elif obj.name.startswith('TEXT_'):
                        apply_widget_transforms(obj, transforms, 'TEXT')
            
            # 본 동기화 실행
            bpy.ops.edit.sync_metarig_bone()
            
    except Exception as e:
        print(f"Error in transform handler: {str(e)}")
