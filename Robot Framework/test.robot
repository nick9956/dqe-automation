*** Settings ***
Library           SeleniumLibrary
Library           helper.py

Suite Setup       Open Browser To Report
Suite Teardown    Close Browser

*** Variables ***
${REPORT_FILE}      file:///${CURDIR}/report.html
${PARQUET_FILE}     ${CURDIR}/parquet_data/facility_type_avg_time_spent_per_visit_date/partition_date=2025-10
${FILTER_COLUMN}    visit_date
${FILTER_VALUE}     2025-10-24
${SORT_COLUMNS}     ['visit_date', 'facility_type']
${COLUMN_SELECTOR}  .y-column
${CELL_SELECTOR}    .cell-text

*** Test Cases ***
Compare HTML Table With Parquet Data
    [Documentation]    Compare HTML table data with Parquet file
    ${df_html}=        Read Table Data   ${COLUMN_SELECTOR}    ${CELL_SELECTOR}
    ${df_parquet}=     Read Parquet File    ${PARQUET_FILE}    ${FILTER_COLUMN}    ${FILTER_VALUE}    ${SORT_COLUMNS}
    ${df_parquet}=     Normalize Visit Date    ${df_parquet}
    ${result}=    Compare Dataframes    ${df_html}    ${df_parquet}
    Run Keyword If    ${result["status"]}    Log    DataFrames match!
    ...               ELSE    Fail    DataFrames do not match! Differences:\n${result["diff"]}

*** Keywords ***
Open Browser To Report
    Open Browser    ${REPORT_FILE}    Chrome
