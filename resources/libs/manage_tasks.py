import logging
from rest_injector import build_fieldwire_headers,send_get_request,send_post_request,send_delete_request
from random import randint
from urls import URL,PROJECT_PATH,TASKS_PATH

mylogger = logging.getLogger(__name__)


def create_task_by_projectid(project_id,payload=None,expect_status_code=201):
    """Create task for a project using project id

    Args:
        project_id (int): Project to create the task
        task_name (str, optional): Task name. buit automatically if value is None.
        expect_status_code (int, optional): expected status. Defaults to 201.

    Returns:
        Object: requests.Response object
    """    
    headers =build_fieldwire_headers()
    user_id = headers["fieldwire-user-id"]
    if payload is None:
        mylogger.info("Build minimal payload")
        task_name = f"mytask_{randint(10000, 99999)}"
        payload = {
                        "owner_user_id": user_id,
                        "priority": 1,
                        "name": task_name,

                    }
    url = f"{URL+PROJECT_PATH}/{project_id}{TASKS_PATH}"
    response = send_post_request(url,headers,payload,expect_status_code)
    return response

def create_batch_tasks(project_id,nb_tasks,payload=None):
    """Tasks Batch creation

    Args:
        project_id (int): Project to create the task
        nb_tasks (int): Amount of task to create
    Returns:
        str: Task ids of created tasks
    """    
    task_id_list = []
    for task in range(nb_tasks):
        response = create_task_by_projectid(project_id,payload)
        task_id = response.json()['id']
        task_id_list.append(task_id)
    return  task_id_list

def get_task_list_by_projectid(project_id,expect_status_code=200,extra_params=None):
    """Get list of all task for a project

    Args:
        project_id (str): search by project id

    Returns:
        list: list of tasks
    """    
    headers =build_fieldwire_headers()
    url = f"{URL+PROJECT_PATH}/{project_id}{TASKS_PATH}"
    if extra_params is not None:
        url += extra_params
    response = send_get_request(url,headers,expect_status_code)
    return response

def delete_task_byId(project_id,task_id,expect_status_code=204):
    """Delete a task using project and task ids

    Args:
        project_id (str): search by project id
        task_id (str): task id 

    Returns:
        Object: requests.Response object
    """    
    headers =build_fieldwire_headers()
    url = f"{URL+PROJECT_PATH}/{project_id}{TASKS_PATH}/{task_id}"
    response = send_delete_request(url,headers,expect_status_code)
    return response

def batch_delete_tasks(project_id,task_ids_list):
    """Delete tasks by list of task id

    Args:
        project_id (str): project_id
        task_ids_list (list): list of tasks ids to be deleted

    Returns:
        tuple: deleted task ids and deletion result
    """    
    deleted_tasks_result = []
    for task_id in task_ids_list:
        response = delete_task_byId(project_id,task_id)
        deleted_tasks_result.append((task_id,response.status_code))
    return deleted_tasks_result
