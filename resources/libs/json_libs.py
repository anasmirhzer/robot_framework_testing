import json, re, logging
from deepdiff import DeepDiff

mylogger = logging.getLogger(__name__)

def compare_json(expected,received):
    compare_result = DeepDiff(expected,received)
    if compare_result == {}:
        return True
    mylogger.error(f"Unmatched response, Expected: {expected}, received: {received}")
    return False

def validate_json_input(json_input):
    """This function converts A json to python dict
    Args:
        json_input str or json
    Returns:
        _type_: Valid dict object
    """
    if not isinstance(json_input,dict):
        try:
            formatted_json = json.loads(json_input)
            mylogger.info("formatted to json %s",type(formatted_json))
            return formatted_json
        except Exception as json_exception:
            mylogger.error("%s -> Invalid json",json_exception)
            raise TypeError("Invalid Json")
    else:
        mylogger.info("is json dict by default %s",json_input)
        return json_input


def flatten_json(input_json, path=[], separator="."):
    """Converts json dict to a flat dict using sub-branches keys by create a unique key
    Args:
        input_json (dict): Json content
        path (list, optional): JsonPath if specified, defaulted to []
        separator (str, optional): Keys separator string. Defaults to "."

    Returns:
        dict: Flat Json dict with unique keys
    """
    result = {}
    for key, value in list(input_json.items()):
        current_path = path + [key]
        if isinstance(value, dict):
            result.update(flatten_json(value, current_path))
        else:
            result[separator.join(current_path)] = value
    return result

def check_json_data(expected_json, json_response):
    """Compares the expected values with any json
    Args:
        expected_values (dict): expected json
        json_response (dict): received json
    Returns:
        bool: True (False for Match function)
    """
    json_response = flatten_json(validate_json_input(json_response))
    expected_values = flatten_json(validate_json_input(expected_json))
    result = True
    try:
        for key in expected_values.keys():
            if str(expected_values[key]).startswith('#regex '):
                expected_values[key] = expected_values[key].replace('#regex ', '')
                if not re.fullmatch(expected_values[key], json_response[key]):
                    mylogger.warning(
                        "Regex did not match for the key: %s Expected regex to be matched: %s Actual parsed string: %s",
                         key, expected_values[key], json_response[key]
                    )
                    result = False
            elif expected_values[key] != json_response[key]:
                mylogger.warning(
                    "Failing match for the key: %s Expected result: %s Actual result: %s"
                    , key, expected_values[key], json_response[key]
                )
                result = False
    except KeyError as key_path:
        mylogger.error("Key does not exist : %s", key_path)
        result = False
    return result

def get_json_data(list_keys, json_response):
    """retreives data based on keyPath and json received
    Args:
        list_keys (list): list of flat path
        json_response (dict): received json
    Returns:
        dict: dictionary with info
    """
    if not isinstance(list_keys, list):
        raise TypeError("Input is not list")
    json_response = flatten_json(validate_json_input(json_response))
    output_dict = {}
    for key in list_keys:
        try:
            output_dict[key] = json_response[key]
        except KeyError as key_path:
            raise KeyError("Key not found", key_path)
    return output_dict

def override_json(json_input,data_dict):
    """Override Json with custom data from another data dict

    Args:
        json_input (dict): input json
        data_dict (dict): dict containing data 

    Returns:
        dict: Overriden json
    """    
    for key in data_dict.keys():
        json_input[key] = data_dict[key]
    return json_input

