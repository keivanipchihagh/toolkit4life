# Standard imports
from sqlalchemy import create_engine
from pandas import DataFrame, read_sql_query


class PostgresClient():

    def __init__(self, host: str, port: str, database: str, username: str, password: str) -> None:
        """
            Creates and initializes a PostgreSQL engine instance that connects to the database

            Parameters:
                host (str): Host IP address
                port (str): Port number
                database (str): Name of the database
                username (str): Username for authentication/privileges
                password (str): Password for authentication
        """

        self.engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")


    def _select(self, query: str, index_col: str = None) -> DataFrame:
        """ Executes the given query and returns the results as a DataFrame """
        return read_sql_query(sql = query, con = self.engine, index_col = index_col)


    def _insert(self, df: DataFrame, name: str, if_exists: str = "append", index: bool = False,index_label: str = None) -> None:
        """
            Inserts the given DataFrame into the database

            Parameters:
                df (DataFrame): The data to be inserted
                name (str): The name of the table to insert the dataframe into
                if_exists (str): Whether to append to the existing table if it exists or create a new one
                index (bool): Whether to drop the index
                index_label (str): The name of the index column
        """
        df.to_sql(name, con = self.engine, if_exists = if_exists, index = index, index_label = index_label)