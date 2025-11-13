*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  kalle
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  ka
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Click Button  Register
    Page Should Contain Error  Username must be at least 3 characters

Register With Valid Username And Too Short Password
    Set Username  kalle
    Set Password  short
    Set Password Confirmation  short
    Click Button  Register
    Page Should Contain Error  Password must be at least 8 characters

Register With Valid Username And Invalid Password
    Set Username  kalle
    Set Password  password
    Set Password Confirmation  password
    Click Button  Register
    Page Should Contain Error  Password must include at least one number

Register With Nonmatching Password And Password Confirmation
    Set Username  kalle
    Set Password  kalle123
    Set Password Confirmation  kalle12
    Click Button  Register
    Page Should Contain Error  Passwords do not match

Register With Username That Is Already In Use
    Create User  kalle  kalle123
    Go To Register Page
    Set Username  kalle
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Click Button  Register
    Page Should Contain Error  Username already exists

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Reset Application And Go To Register Page
    Reset Application
    Go To Register Page
