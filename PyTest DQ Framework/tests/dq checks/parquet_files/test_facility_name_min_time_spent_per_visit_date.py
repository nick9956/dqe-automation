"""
Description: Data Quality checks ...
Requirement(s): TICKET-1234
Author(s): Name Surname
"""
import pytest
from src.types import facility_name_min_time_spent_per_visit_date_type
from src.helpers import cast_columns

@pytest.fixture(scope='module')
def target_data(db_connection):
    target_query = """
    SELECT
      f.facility_name,
      DATE(v.visit_timestamp) AS visit_date,
      MIN(v.duration_minutes) AS min_time_spent
    FROM
      visits AS v
    JOIN
     facilities AS f ON f.id = v.facility_id
    GROUP BY
      f.facility_name,
      visit_date;
    """
    target_data = db_connection.get_data_sql(target_query, dtype=facility_name_min_time_spent_per_visit_date_type)
    return target_data

@pytest.fixture(scope='module')
def source_data(parquet_reader):
    source_path = '/parquet_data/facility_name_min_time_spent_per_visit_date'
    print(f"Trying to load parquet files from: {source_path}")
    parquet_reader.process(source_path, include_subfolders=True)
    df = parquet_reader.get_dataframe()
    df = cast_columns(df, facility_name_min_time_spent_per_visit_date_type)
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