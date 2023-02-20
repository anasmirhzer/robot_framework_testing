import requests
from token_generator import render_token_elements

def build_fieldwire_headers():
    auth_token,user_id= render_token_elements()
    headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "fieldwire-user-token": auth_token,
            "fieldwire-user-id": str(user_id)
        }
    return headers


def check_http_status(http_response,expect_status_code=None):
    """_summary_

    Args:
        http_response: response http object
        expect_status_code (int, optional): expected status code. Defaults to None.

    Raises:
        ValueError: Status different than expected value
    """    
    if expect_status_code is not None and http_response.status_code != expect_status_code:
        raise  ValueError(f"Unexpected response {http_response.status_code}, {http_response.text}") 

def send_post_request(url,headers,payload,expect_status_code=None):
    response = requests.post(url, json=payload, headers=headers)
    check_http_status(response,expect_status_code)
    return response

def send_get_request(url,headers,expect_status_code=None):
    response = requests.get(url, headers=headers)
    check_http_status(response,expect_status_code)
    return response

def send_delete_request(url,headers,expect_status_code=None):
    response = requests.delete(url, headers=headers)
    check_http_status(response,expect_status_code)
    return response

