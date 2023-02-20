*** Settings ***
Library         JSONLibrary
Library         ../../resources/libs/json_libs.py
Library         ../../resources/libs/manage_project.py
Library         ../../resources/libs/manage_tasks.py
Variables       ../../resources/data/common_data.py


*** Keywords ***
Load Data Set
    [Arguments]    ${Test_scenario_folder}    ${file_name}
    ${dataset}    Load Json From File
    ...    ${EXECDIR}/${data_set_path}/${Test_scenario_folder}/${file_name}
    RETURN    ${dataset}

Load and Override Data Set
    [Arguments]    ${Test_scenario_folder}    ${file_name}    ${override_dict}
    ${dataset}    Load Json From File
    ...    ${EXECDIR}/${data_set_path}/${Test_scenario_folder}/${file_name}
    ${overriden_dataset}    Override Json    ${dataset}    ${override_dict}
    RETURN    ${overriden_dataset}

Check Exact Match Json
    [Arguments]    ${expected_response}    ${received_response}
    ${response_check}    Compare Json    ${expected_response}    ${received_response}
    ${response_check}    Should Be True    ${response_check}

Check Json Response
    [Arguments]    ${expected_response}    ${received_response}
    ${response_check}    check_json_data    ${expected_response}    ${received_response}
    Should Be True    ${response_check}

Create project and Get id
    ${response}    manage_project.create_project
    Log    ${response.json()["id"]}
    Set Suite Variable    ${project_id}    ${response.json()["id"]}

Create Tasks and Get ids
    [Arguments]    ${project_id}    ${nb_tasks}    ${payload}=${None}
    ${tasks}    manage_tasks.create_batch_tasks    ${project_id}    ${nb_tasks}    ${payload}
    Set Test Variable    ${tasks_ids_list}    ${tasks}

Check List Length
    [Arguments]    ${list}    ${expected_length}
    ${length}    Get Length    ${list}
    Should Be Equal As Integers    ${length}    2
