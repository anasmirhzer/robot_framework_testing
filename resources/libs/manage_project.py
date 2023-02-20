import logging
from rest_injector import build_fieldwire_headers,send_delete_request,send_get_request,send_post_request
from random import randint
from urls import URL,PROJECT_PATH

mylogger = logging.getLogger(__name__)

def create_project(payload=None,expect_status_code=201):
    """Create a new project with a project name

    Args:
        project_name (str, optional): Project name. Generated automatically by Default.
        expect_status_code (int, optional): expected http status. Defaults to 201.
    Returns:
        Object: requests.Response object.
    """    
    headers =build_fieldwire_headers()
    url = URL+PROJECT_PATH
    if payload is None:
        project_name = f"myproject_{randint(10000, 99999)}"
        mylogger.info("Build minimal payload")
        payload = {
                    "project": 
                        {
                            "name": project_name
                        }
                    }

    response = send_post_request(url,headers,payload,expect_status_code)
    return response

#Get project by name ?filters[name_like]=myproject

def get_projects_list():
    """Get project status

    Args:
        project_status (str): filter by Project status (Not working as designed, always returns full list)

    Returns:
        list: list of dicts
    """    
    headers =build_fieldwire_headers()
    url =URL+PROJECT_PATH
    response = send_get_request(url,headers)
    return response


def get_active_project_ids():
    """Get active project ids
        work around to get list projects 
    Returns:
        list: list of active projects ids
    """    
    project_list= get_projects_list().json()
    active_projects_list = [(element["id"]) for element in project_list if element["deleted_at"] is None]
    return active_projects_list
    

def delete_project(project_id,expected_status_code=204):
    """Delete project by id

    Args:
        project_id (str): Id of project to be deleted
        expected_status_code (int, optional): expected status to match. Defaults to 204.
    Returns:
        Object: requests.Response object.
    """    
    headers =build_fieldwire_headers()
    url = f"{URL+PROJECT_PATH}/{project_id}"
    response = send_delete_request(url,headers,expected_status_code)
    return response

def clean_account_projects():
    """Delete all active projects for the account

    Returns:
        Bool: True if all projects are succesfully deleted
    """    
    deleted_projects = []
    not_deleted_projects = []
    projects_to_clean = get_active_project_ids()
    
    for project in projects_to_clean:
        delete_result = delete_project(project).status_code
        if delete_result == 204:
            deleted_projects.append((project))
        else:
            not_deleted_projects.append((project))

    if len(deleted_projects) != len(projects_to_clean):
        mylogger.error(f"Projects clean up failure: Deleted: {deleted_projects}, Not deleted: {not_deleted_projects}")
        return False
    mylogger.info(f"Projects clean up succes: {deleted_projects}")
    return True

