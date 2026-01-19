import pandas as pd
import os
import glob


class ParquetReader:
    def __init__(self):
        """
        Initialize the ParquetReader with the path to the Parquet file.
        """
        self.dataframe = None

    def process(self, file_path, include_subfolders=False):
        try:
            if include_subfolders and os.path.isdir(file_path):
                # Recursively find all .parquet files
                parquet_files = glob.glob(os.path.join(file_path, '**', '*.parquet'), recursive=True)
                if not parquet_files:
                    raise FileNotFoundError(f"No parquet files found in {file_path} and subfolders.")
                # Concatenate all found parquet files
                self.dataframe = pd.concat([pd.read_parquet(f) for f in parquet_files], ignore_index=True)
            else:
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
