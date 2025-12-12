import pytest
import pandas as pd
from datetime import datetime

# Fixture to read the CSV file
@pytest.fixture(scope="session")
def csv_data(request):
    path_to_file = request.config.getoption("--csv-file")
    df = pd.read_csv(path_to_file)
    return df

# Fixture to validate the schema of the file
@pytest.fixture(scope="session")
def validate_schema():
    def _validate_schema(actual_schema, expected_schema):
        errors = []

        # Check column names
        if list(actual_schema.keys()) != list(expected_schema.keys()):
            errors.append(f"Column names mismatch. "
                          f"Expected: {list(expected_schema.keys())}, Got: {list(actual_schema.keys())}")

        # Check data types
        for column, expected_type in expected_schema.items():
            actual_type = actual_schema.get(column, None)
            if actual_type != expected_type:
                errors.append(f"Column '{column}' has incorrect type. "
                              f"Expected: {expected_type}, Got: {actual_type}")

        return {"is_valid": len(errors) == 0, "errors": errors}

    return _validate_schema

# Pytest hook to mark unmarked tests with a custom mark
def pytest_collection_modifyitems(session, config, items):
    for item in items:
        if not list(item.iter_markers()):
            item.add_marker('unmarked')


def pytest_configure(config):
        if not config.option.htmlpath:
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            config.option.htmlpath = f"reports/report_{now}.html"

def pytest_addoption(parser):
    parser.addoption(
        "--csv-file",
        action="store",
        default="./../src/data/data.csv",
        help="Path to the CSV file to be loaded for tests"
    )
