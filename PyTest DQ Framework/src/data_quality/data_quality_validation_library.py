import pandas as pd


class DataQualityLibrary:
    """
    A library of static methods for performing data quality checks on pandas DataFrames.

    This class is intended to be used in a PyTest-based testing framework to validate
    the quality of data in DataFrames. Each method performs a specific data quality
    check and uses assertions to ensure that the data meets the expected conditions.
    """

    @staticmethod
    def check_duplicates(df):
            return not df.duplicated().any()

    @staticmethod
    def check_count(df1, df2):
        if df1 is None or df2 is None:
            return False
        return len(df1) == len(df2)

    @staticmethod
    def check_data_completeness(source_data, target_data):
        merged = source_data.merge(target_data.drop_duplicates(), how='left', indicator=True)
        return (merged['_merge'] != 'left_only').all()

    @staticmethod
    def check_dataset_is_not_empty(df):
        return not df.empty

    @staticmethod
    def check_not_null_values(df, column_names=None):
        if column_names is None:
            column_names = df.columns.tolist()
        else:
            if not all(col in df.columns for col in column_names):
                return False
        result = {}
        for col in column_names:
            result[col] = df[col].notnull().all()
        # Return True only if all columns have no nulls, otherwise False
        return all(result.values())