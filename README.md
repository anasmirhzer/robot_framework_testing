# Robot_framework_testing for FIELDWIRE APIs
## Environment setup
**1. Create Python env :**
 python3 -m venv env
 
**2. Intall framework requirement :** 
 pip install -r requirement.txt

**3. Intall robot framework extensions:** 
 Robot Framework Language Server

**4. launch.json file config (Run Robot Tests via Vscode) :** 
```
{
    "configurations": [
        {
            "type": "robotframework-lsp",
            "name": "Robot Framework: Launch Template",
            "request": "launch",
            "terminal": "integrated",
            // Agrument to run tests using extensions
            "args": [
                "--loglevel",
                "DEBUG",
                "--outputdir",
                "${workspaceFolder}/reports",
                "-i",
                "${input:tag}"
            ]
        }
    ],
    // Select type of tests based on Tags defined in test cases
    "inputs": [
        {
            "id": "tag",
            "type": "pickString",
            "description": "choose test compaign",
            "options": [
                "all",
                "smoke_test",
                "regression_test",
                "error_case",
                "bugged_test"
            ],
            "default": "regression_test"
        }
    ]
}
```

**5. Define secret user data** :
 Create a .env file in root directory
```
EMAIL=xxxxxxx@xxxx.xx
PASSWORD=XXXXXXXXXX
ACCOUNT_NUM=XXXXXX
ACCOUNT_NAME=XXXXXX
USER_ID=XXXXXXX  
```
## Run Tests

**Vscode: Run from lab section and select test level and type** :


**CLI: Run all test suites, generate report** :
 robot --outputdir reports  tests 

**CLI: Run test suites (Only smoke tests), generate report** :
 robot --outputdir reports  -i smoke_test  tests 

**CLI: Run all test suites exluding tests using Tag, generate report** :
 robot --outputdir reports  -e bugged_test  tests

## Identified issues/bugs
 1. **Wrong header name for access token in API Reference:**
    - Authorization instead of fieldwire-user-token
 2. **Filtering not correctly working from the API:**
    - Filter for tasks and project list retrieves full list ( Works from the UI)
    - Example in tests tagged as bugged_test
 3. **Improvement suggestions:**
    - Filtering by active/intactive/deleted projects and tasks

