from resources.data.common_data import id_regex,timestamp_regex,account_email,account_id,account_name,token_id_regex


# Project data dict
create_project_output_data = {
    "created_at":timestamp_regex,
    "updated_at":timestamp_regex,
    "device_created_at":timestamp_regex,
    "device_updated_at":timestamp_regex,
    "account_id":account_id,
    "id":id_regex,
    "owner_email":account_email,
    "account_name":account_name,
    "access_token":token_id_regex
                             }