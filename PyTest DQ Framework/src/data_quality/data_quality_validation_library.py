import pandas as pd


class DataQualityLibrary:
    """
    A library of static methods for performing data quality checks on pandas DataFrames.

    This class is intended to be used in a PyTest-based testing framework to validate
    the quality of data in DataFrames. Each method performs a specific data quality
    check and uses assertions to ensure that the data meets the expected conditions.
    """

    @staticmethod
    def check_duplicates(df, column_names=None):
        if column_names:
            return df.duplicated(subset=column_names).any()
        else:
            return df.duplicated().any()

    @staticmethod
    def check_count(df1, df2):
        return len(df1) == len(df2)

    @staticmethod
    def check_data_completeness(source_data, target_data):
        source_data['visit_date'] = pd.to_datetime(source_data['visit_date'])
        target_data['visit_date'] = pd.to_datetime(target_data['visit_date'])
        merged = source_data.merge(target_data.drop_duplicates(), how='left', indicator=True)
        return (merged['_merge'] != 'left_only').all()

    @staticmethod
    def check_dataset_is_not_empty(df):
        return not df.empty

    @staticmethod
    def check_not_null_values(df, column_names=None):
        if column_names is None:
            column_names = df.columns.tolist()
        result = {}
        for col in column_names:
            result[col] = df[col].notnull().all()
        return result