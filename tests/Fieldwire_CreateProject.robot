*** Settings ***
Library         ../resources/libs/manage_project.py
Resource        ../resources/models/technical_model.robot
Variables       ../resources/data/testdata/create_project/data.py

Suite Setup     clean_account_projects


*** Variables ***
${Invalid_request}      create_project/invalid_request
${full_check}           create_project/full_check


*** Test Cases ***
Create Project response status check - Test OK
    [Tags]    smoke_test    all
    create_project

Create Project full options - Test OK
    [Tags]    regression_test    all
    ${Request_body}    Load Data Set    ${full_check}    input_json.json
    ${expected_response}    Load and Override Data Set
    ...    ${full_check}
    ...    output_json.json
    ...    ${create_project_output_data}
    ${received_response}    create_project    payload=${Request_body}
    Check Json Response    ${expected_response}    ${received_response.json()}

Create Project - Test KO Invalid request
    [Tags]    regression_test    error_cases    all
    ${Request_body}    Load Data Set    ${Invalid_request}    input_json.json
    ${expected_response}    Load Data Set    ${Invalid_request}    output_json.json
    ${received_response}    create_project    payload=${Request_body}    expect_status_code=${422}
    Check Exact Match Json    ${expected_response}    ${received_response.json()}
