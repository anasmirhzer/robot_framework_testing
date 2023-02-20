*** Settings ***
Library         ../resources/libs/manage_project.py
Library         ../resources/libs/manage_tasks.py
Resource        ../resources/models/technical_model.robot
Variables       ../resources/data/testdata/create_task/data.py

Suite Setup     Run Keywords    clean_account_projects    Create project and Get id


*** Variables ***
${Invalid_request}      create_task/invalid_request
${full_check}           create_task/full_check


*** Test Cases ***
Create Task response status check - Test OK
    [Tags]    smoke_test    all
    create_task_by_projectid    ${project_id}

Create task full check - Test OK
    [Tags]    regression_test    all
    ${Request_body}    Load and Override Data Set    ${full_check}    input_json.json    ${create_task_input_data}
    ${expected_response}    Load and Override Data Set
    ...    ${full_check}
    ...    output_json.json
    ...    ${create_task_output_data}
    ${received_response}    create_task_by_projectid    project_id=${project_id}    payload=${Request_body}
    Check Json Response    ${expected_response}    ${received_response.json()}

Create Task - Test KO Invalid request
    [Tags]    regression_test    error_case    all
    ${Request_body}    Load Data Set    ${Invalid_request}    input_json.json
    ${expected_response}    Load Data Set    ${Invalid_request}    output_json.json
    ${received_response}    create_task_by_projectid
    ...    project_id=${project_id}
    ...    payload=${Request_body}
    ...    expect_status_code=${422}
    Check Exact Match Json    ${expected_response}    ${received_response.json()}
