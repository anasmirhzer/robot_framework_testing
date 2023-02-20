# This script aims at extracting the user id and user authentication token based
# on the provided email and password. It then uses the retrieved credentials to
# make a sample call to the API 'current_user' endpoint.
#
# Pre-requisite:
#  - install the "requests" Python lib: `pip3 install requests`
#
# Run the script:
#  `python3 user_authent_info_extractor.py USER_EMAIL_ADDRESS USER_PASSWORD`
#
# Use the returned authentication token and user id to call the API typically
# like this:
# ```
# curl https://app.fieldwire.com/api/v3/... \
#     -H 'Fieldwire-User-Token: AUTH_TOKEN' \
#     -H 'Fieldwire-User-Id: USER_ID' \
#     -H 'Content-Type: application/json' \
#     -H 'Fieldwire-Version: 2020-06-22'
# ```
#
import  sys, requests, logging, os

from dotenv import dotenv_values
from urls import URL,SIGN_IN_PATH

mylogger = logging.getLogger(__name__)
config = dotenv_values(".env")

def generate_access_token(email=config['EMAIL'],password=config['PASSWORD'],set_env_variables=True):
    # define a params dict for the parameters to be sent to the API
    PARAMS = {'user_login': {'email': email, 'password': password}}
    HEADERS = {'Fieldwire-Version': "2020-06-22", 'Content-Type': "application/json"}

    # send request
    r = requests.post(URL + SIGN_IN_PATH, json=PARAMS, headers=HEADERS)

    # extract data in json format
    data = r.json()
    if not "auth_token" in data:
        mylogger.error("ERROR: no auth_token in {0}".format(data))
        sys.exit(-1)
    if not "user" in data or not "id" in data["user"]:
        mylogger.error("ERROR: no user nor id in {0}".format(data["user"]))
        sys.exit(-1)
    # extract credentials
    auth_token = data["auth_token"]
    user_id = data["user"]["id"]
    if set_env_variables:
        os.environ['auth_token'] = str(auth_token)
        os.environ['user_id'] = str(user_id)
    return auth_token,user_id

def render_token_elements():
    auth_token,user_id = os.getenv('auth_token'), os.getenv('user_id')
    if not auth_token and not user_id:
        mylogger.info("No Token in Env variables, generate Token")
        return generate_access_token()
    mylogger.info(f"Token available in env variables, auth_token:{auth_token}, user_id:{user_id}")
    return auth_token,user_id
    



    
                              
