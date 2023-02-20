*** Settings ***
Library             ../resources/libs/manage_project.py
Library             ../resources/libs/manage_tasks.py
Resource            ../resources/models/technical_model.robot
Variables           ../resources/data/testdata/list_tasks/data.py

Suite Setup         Run Keywords    clean_account_projects    Create project and Get id
Test Setup          Create Tasks and Get Ids    ${project_id}    ${3}
Test Teardown       batch delete tasks    project_id=${project_id}    task_ids_list=${tasks_ids_list}


*** Variables ***
${Invalid_request}          list_tasks/invalid_request
${Check_content}            list_tasks/Check_content
${Create_task_payload}      list_tasks/filter_by_name


*** Test Cases ***
List tasks response status check - Test OK
    [Tags]    smoke_test    all
    get_task_list_by_projectid    ${project_id}

List task Check content - Test OK
    [Tags]    regression_test    all
    [Setup]    Create Tasks and Get Ids    ${project_id}    ${1}
    ${expected_response}    Load and Override Data Set
    ...    ${Check_content}
    ...    output_json.json
    ...    ${list_task_output_data}
    ${received_response}    get_task_list_by_projectid    project_id=${project_id}
    Check Json Response    ${expected_response}    ${received_response.json()[0]}

List task - filter by task name - Test OK
    [Tags]    bugged_test    all
    ${Request_body}    Load and Override Data Set
    ...    ${Create_task_payload}
    ...    input_json.json
    ...    ${create_task_input_data}
    Create Tasks and Get Ids    ${project_id}    ${2}    ${Request_body}
    ${received_response}    get_task_list_by_projectid
    ...    project_id=${project_id}
    ...    expect_status_code=${200}
    ...    extra_params=?filters[name_eq]=my_task_filterName
    Log    ${received_response.json()}
    Check List Length    ${received_response.json()}    ${2}

List tasks - Test KO Invalid Request Wrong Project id
    [Tags]    regression_test    error_case    all
    ${received_response}    get_task_list_by_projectid    project_id=toto    expect_status_code=${404}
    ${expected_response}    Load Data Set    ${Invalid_request}    output_json.json
    Check Exact Match Json    ${expected_response}    ${received_response.json()}
