*** Settings ***
Documentation           A test suite for testing the library can be imported
Library                 lisacattools

*** Variables ***
${name}                 lisacattools
${version}              1.1.1

*** Test Cases ***
Test library name
    Library name should be equal to     ${name}

Test library version
    Library version should be equal to  ${version}


*** Keywords ***
Library name should be equal to
    [Arguments]         ${name_arg}
    ${lib}=             Get Library Instance            lisacattools
    Should Be Equal     ${lib.__name__}                 ${name_arg}

Library version should be equal to
    [Arguments]         ${version_arg}
    ${lib}=             Get Library Instance            lisacattools
    Should Be Equal     ${lib.__version__}              ${version_arg}
