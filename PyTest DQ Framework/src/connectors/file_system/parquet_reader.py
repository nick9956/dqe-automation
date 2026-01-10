import pandas as pd


class ParquetReader:
    def __init__(self, file_path):
        """
        Initialize the ParquetReader with the path to the Parquet file.
        """
        self.file_path = file_path
        self.dataframe = None

    def read(self):
        """
        Reads the Parquet file and loads it into a pandas DataFrame.
        """
        try:
            self.dataframe = pd.read_parquet(self.file_path)
            print(f"Successfully loaded {self.file_path}")
        except Exception as e:
            print(f"Error reading Parquet file: {e}")

    def get_dataframe(self):
        """
        Returns the loaded DataFrame.
        """
        if self.dataframe is not None:
            return self.dataframe
        else:
            print("No DataFrame loaded. Call read() first.")
            return None
