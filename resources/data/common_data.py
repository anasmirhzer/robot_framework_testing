from dotenv import dotenv_values

# User account data
user_data = dotenv_values(".env")
account_email = user_data['EMAIL']
account_id = int(user_data['ACCOUNT_NUM'])
user_id = int(user_data['USER_ID'])
account_name = user_data['ACCOUNT_NAME']
user_ids = [user_id]

# Data set Path
data_set_path = "resources/data/testdata"

# Common regex
timestamp_regex = "#regex ^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}(?:\.\d*)?)((-(\d{2}):(\d{2})|Z)?)$"
id_regex = "#regex ^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}$"
token_id_regex = "#regex ^[a-zA-Z0-9_]{32}"







