"""
Description: Data Quality checks ...
Requirement(s): TICKET-1234
Author(s): Name Surname
"""
import os
import pytest

@pytest.fixture(scope='module')
def target_data(db_connection):
    target_query = """
    SELECT * FROM visits
    """
    target_data = db_connection.get_data_sql(target_query)
    return target_data

@pytest.fixture(scope='module')
def source_data(parquet_reader):
    # List all files in the current working directory (before)
    print("Files in current working directory BEFORE:")
    for root, dirs, files in os.walk('.'):
        for name in files:
            print(os.path.join(root, name))

    source_path = 'parquet_data/facility_name_min_time_spent_per_visit_date'
    print(f"Trying to load parquet files from: {source_path}")

    # List all files in the target folder (after)
    if os.path.exists(source_path):
        print(f"Files in {source_path} AFTER:")
        for root, dirs, files in os.walk(source_path):
            for name in files:
                print(os.path.join(root, name))
    else:
        print(f"Path {source_path} does not exist!")

    parquet_reader.process(source_path, include_subfolders=True)
    df = parquet_reader.get_dataframe()
    print(f"Loaded DataFrame: {df}")
    return df

@pytest.mark.parquet_data
@pytest.mark.smoke
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_check_dataset_is_not_empty(target_data, data_quality_library):
    data_quality_library.check_dataset_is_not_empty(target_data)


@pytest.mark.parquet_data
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_check_data_completeness(source_data, target_data, data_quality_library):
    data_quality_library.check_data_completeness(source_data, target_data)

@pytest.mark.parquet_data
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_check_count(source_data, target_data, data_quality_library):
    data_quality_library.check_count(source_data, target_data)

@pytest.mark.parquet_data
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_check_uniqueness(target_data, data_quality_library):
    data_quality_library.check_duplicates(target_data)

@pytest.mark.parquet_data
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_check_not_null_values(target_data, data_quality_library):
    data_quality_library.check_not_null_values(target_data, ['facility_name',
                                                             'visit_date',
                                                             'min_time_spent'])