import pandas as pd


class ParquetReader:
    def __init__(self):
        """
        Initialize the ParquetReader with the path to the Parquet file.
        """
        self.dataframe = None

    def process(self, file_path):
        """
        Reads the Parquet file and loads it into a pandas DataFrame.
        """
        try:
            self.dataframe = pd.read_parquet(file_path)
            print(f"Successfully loaded {file_path}")
        except Exception as e:
            print(f"Error processing Parquet file: {e}")

    def get_dataframe(self):
        """
        Returns the loaded DataFrame.
        """
        if self.dataframe is not None:
            return self.dataframe
        else:
            print("No DataFrame loaded. Call process() first.")
            return None
