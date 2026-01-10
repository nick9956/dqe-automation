import psycopg2
import pandas as pd
from typing import Optional, Type, Any, Dict


class PostgresConnectorContextManager:

    def __init__(self, db_host: str, db_name: str, db_user: str, db_pass: str, db_port: int = 5432):
        """Initializes the connector with database credentials."""
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass

        # Initialize connection and cursor to None. They will be set in __enter__.
        self.connection: Optional[psycopg2.extensions.connection] = None
        self.cursor: Optional[psycopg2.extensions.cursor] = None

    def __enter__(self) -> 'PostgresConnectorContextManager':

        try:
            self.connection = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_pass
            )
            self.cursor = self.connection.cursor()
            return self
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL database: {e}")
            # Re-raise the exception to prevent entering the 'with' block's body
            raise

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException],
                 exc_tb: Optional[Any]):

        if self.connection:
            try:
                if exc_type:
                    # An error occurred, roll back the transaction
                    print(f"An exception of type {exc_type.__name__} occurred. Rolling back transaction.")
                    self.connection.rollback()
                else:
                    # No error, commit the transaction
                    self.connection.commit()
            finally:
                # Ensure cursor and connection are always closed
                if self.cursor:
                    self.cursor.close()
                self.connection.close()
                # Set to None to indicate they are closed
                self.cursor = None
                self.connection = None

    def get_data_sql(self, sql: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:

        if not self.connection:
            raise ValueError("Connection is not available. This method must be called within a 'with' block.")

        try:
            df = pd.read_sql_query(sql, self.connection, params=params)
            return df
        except (Exception, psycopg2.Error) as e:
            print(f"Error executing query: {e}")
            # Re-raising allows the __exit__ method to catch it and roll back
            raise

    def execute_sql(self, sql: str, params: Optional[Dict[str, Any]] = None):

        if not self.cursor:
            raise ValueError("Cursor is not available. This method must be called within a 'with' block.")

        try:
            self.cursor.execute(sql, params)
            print(f"Executed command. Rows affected: {self.cursor.rowcount}")
        except (Exception, psycopg2.Error) as e:
            print(f"Error executing command: {e}")
            raise
