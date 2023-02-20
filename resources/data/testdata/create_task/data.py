from resources.data.common_data import id_regex,timestamp_regex,user_id,user_ids


# Create task data 
# Input data dict 
create_task_input_data = {
    "creator_user_id":user_id,
    "last_editor_user_id":user_id,
    "owner_user_id":user_id
    }

#  Output check data dict
create_task_output_data = {
    "created_at":timestamp_regex,
    "updated_at":timestamp_regex,
    "device_created_at":timestamp_regex,
    "device_updated_at":timestamp_regex,
    "latest_component_device_updated_at":timestamp_regex,
    "status_id":id_regex,
    "project_id":id_regex,
    "id":id_regex,
    "task_type_id":id_regex,
    "creator_user_id":user_id,
    "owner_user_id":user_id,
    "last_editor_user_id":user_id,
    "user_ids":user_ids
    }