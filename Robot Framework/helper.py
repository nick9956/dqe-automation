import pandas as pd
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def read_parquet_file(file_path, filter_column: str = None, filter_value: str = None, sorting_columns: list = None):
    try:
        df = pd.read_parquet(file_path, engine='pyarrow')

        # Filter by column and value if provided
        if filter_column and filter_value:
            if filter_column not in df.columns:
                raise ValueError(f"Filter column '{filter_column}' not found in DataFrame columns: {list(df.columns)}")
            df = df.loc[df[filter_column] >= filter_value]

        # Sort by columns if provided
        print(sorting_columns)
        if sorting_columns:
            missing = [col for col in sorting_columns if col not in df.columns]
            if missing:
                raise ValueError(f"Missing columns for sorting: {missing}. DataFrame columns: {list(df.columns)}")
            df = df.sort_values(by=sorting_columns, ascending=False)
        return df
    except Exception as e:
        print(f"Error reading Parquet file: {e}")
        raise

def normalize_visit_date(df):
    if 'visit_date' in df.columns:
        df['visit_date'] = pd.to_datetime(df['visit_date']).dt.strftime('%Y-%m-%d')
    return df

def read_table_data(columns_selector, cell_selector, timeout=10):
    selib = BuiltIn().get_library_instance('SeleniumLibrary')
    driver = selib.driver

    # Wait until columns are visible
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR, columns_selector))
    )
    columns = driver.find_elements(By.CSS_SELECTOR, columns_selector)
    columns_data = []
    for col in columns:
        cell_texts = col.find_elements(By.CSS_SELECTOR, cell_selector)
        columns_data.append([t.text for t in cell_texts])

    facility_type = columns_data[0][:-1]
    visit_date = columns_data[1][:-1]
    avg_time_spent = columns_data[2][:-1]

    df = pd.DataFrame({
        'facility_type': facility_type,
        'visit_date': visit_date,
        'avg_time_spent': avg_time_spent
        })

    df['avg_time_spent'] = pd.to_numeric(df['avg_time_spent'], errors='coerce').round(2)

    return df

def compare_dataframes(df1, df2):
    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)

    equals = df1.equals(df2)
    if equals:
        return {"status": True, "diff": None}
    else:
        diff1 = df1[~df1.apply(tuple, 1).isin(df2.apply(tuple, 1))]
        diff2 = df2[~df2.apply(tuple, 1).isin(df1.apply(tuple, 1))]
        diff = pd.concat([diff1, diff2])
        return {"status": False, "diff": diff.to_string()}
