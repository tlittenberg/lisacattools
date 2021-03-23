*** Settings ***
Documentation           A test suite for testing the import of plugin
Library                 lisacattools.plugins.mbh.MbhCatalogs   ${dir_data}                          WITH NAME   mbhCat
Library                 lisacattools.plugins.mbh.MbhCatalog    ${cat_name}     ${cat_location}      WITH NAME   cat_mbh
Library                 lisacattools.GWCatalogType                                                  WITH NAME   GWCatalogType
Library                 TestPluginMbh.py                                                            WITH NAME   test_create_mbh
Library                 TestPluginUcb.py                                                            WITH NAME   test_create_ucb
Library                 TestCacheDoesNotCacheWrongElt.py                                            WITH NAME   cache

*** Variables ***
${dir_data}             tutorial/data/mbh
${cat_name}             MBHcatalog_week001
${cat_location}         tutorial/data/mbh/MBH_wk001C.h5

*** Test Cases ***
Test LISA Plugin Exists
    Check LISA Plugin Exists

Test Catalogs Object With LISA Plugin
    The Module Of The LISA Plugin Should Be             lisacattools.plugins.mbh
    The Class Of The LISA Plugin Should Be              MbhCatalogs
    Metadata Should Exist
    The Number Of Catalogs Should Be                    14
    The First Catalog Should Be                         MBHcatalog_week001
    The Last Catalog Should Be                          MBHcatalog_week015
    The Catalog MBHcatalog_week003 Should Be            MBHcatalog_week003

Test MBHcatalog_week001 Catalog With LISA Plugin
    The Name Of The Catalog Should Be                   MBHcatalog_week001
    The Location Of The Catalog Should Be               ${dir_data}/MBH_wk001C.h5
    The Number Of Detections Should Be                  1
    ${detections_attr}=                                 Create List     Parent    Log Likelihood    Mass 1    Mass 2    Spin 1    Spin 2    Merger Phase    Barycenter Merge Time     Luminosity Distance   cos ecliptic colatitude     Ecliptic Longitude    Polarization      cos inclination   Detector Merger Time      Ecliptic Latitude     chain file
    The Attributes in Detections Should Be              ${detections_attr}

Test creation of Plugins
    The List Of Files With MBH Should Be                14
    The List Of Files With UCB Should Be                2

Test cache does not cache wrong elts
    The Elts Should Be Cached                           False

*** Keywords ***
Check LISA Plugin Exists
    ${lib}=                         Get Library Instance            GWCatalogType
    ${lisa} =                       Set Variable                    ${lib.MBH}

The Module Of The LISA Plugin Should Be
    [Arguments]                     ${name}
    ${lib}=                         Get Library Instance            GWCatalogType
    ${lisa} =                       Set Variable                    ${lib.MBH}
    Should Be Equal                 ${lisa.module_name}             ${name}

The Class Of The LISA Plugin Should Be
    [Arguments]                     ${name}
    ${lib}=                         Get Library Instance            GWCatalogType
    ${lisa} =                       Set Variable                    ${lib.MBH}
    Should Be Equal                 ${lisa.class_name}             ${name}

Metadata Should Exist
    ${lib}=                         Get Library Instance            mbhCat
    Set Test Variable               ${lib.metadata}

The Number Of Catalogs Should Be
    [Arguments]                     ${nb_cat}
    ${lib}=                         Get Library Instance            mbhCat
    Should Be Equal As Numbers      ${lib.count}                    ${nb_cat}

The First Catalog Should Be
    [Arguments]                     ${name}
    ${cnt}=                         Get first catalog
    Should Be Equal                 ${cnt.name}                     ${name}

The Last Catalog Should Be
    [Arguments]                     ${name}
    ${cnt}=                         Get last catalog
    Should Be Equal                 ${cnt.name}                     ${name}

The Catalog MBHcatalog_week003 Should Be
    [Arguments]                     ${name}
    ${cnt}=                         Get catalog by                  MBHcatalog_week003
    Should Be Equal                 ${cnt.name}                     ${name}

The Name Of The Catalog Should Be
    [Arguments]                     ${name}
    ${lib}=                         Get Library Instance            cat_mbh
    Should Be Equal                 ${lib.name}                     ${name}

The Location Of The Catalog Should Be
    [Arguments]                     ${location}
    ${lib}=                         Get Library Instance            cat_mbh
    Should Be Equal                 ${lib.location}                 ${location}

The Number Of Detections Should Be
    [Arguments]                     ${nb_detections}
    ${cnt}=                         Get detections
    ${cnt_len}=                     Get length                      ${cnt}
    Should Be Equal As Numbers      ${cnt_len}                      ${nb_detections}

The Attributes in Detections Should Be
    [Arguments]                     ${attributes}
    ${cnt}=                         Get attr detections
    Should Be Equal                 ${cnt}                          ${attributes}

The List Of Files With MBH Should Be
    [Arguments]                     ${nb}
    ${result}=	                    Convert To Integer	            ${nb}
    ${cnt}                          test_create_mbh.Get Number
    Should Be Equal                 ${cnt}                          ${result}

The List Of Files With UCB Should Be
    [Arguments]                     ${nb}
    ${result}=	                    Convert To Integer	            ${nb}
    ${cnt}                          test_create_ucb.Get Number
    Should Be Equal                 ${cnt}                          ${result}

The Elts Should Be Cached
    [Arguments]                     ${expected_result}
    ${result}=                      Convert To Boolean              ${expected_result}
    ${cnt}                          cache.Get Equal
    Should Be Equal                 ${cnt}                          ${result}