# Standard imports
import sqlalchemy
from pandas import DataFrame, read_sql_query
from sqlalchemy_utils.functions import database_exists, create_database


class SQLAlchemy():

    def __init__(self, engine: str, host: str, port: str, database: str, username: str, password: str) -> None:
        """
            Creates and initializes a PostgreSQL engine instance that connects to the database

            Parameters:
                engine (str): The name of the database engine (postgres, trino, etc.)
                host (str): Host IP address
                port (str): Port number
                database (str): Name of the database
                username (str): Username for authentication/privileges
                password (str): Password for authentication
        """
        self.engine = engine
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database


    def _select(self, query: str, index_col: str = None) -> DataFrame:
        """ Executes the given query and returns the results as a DataFrame """
        return read_sql_query(sql = query, con = self.engine, index_col = index_col)


    def _execute(self, query: str) -> None:
        """ Executes the given query """
        self.engine.execute(query)


    def table_exists(self, name: str) -> bool:
        """ Checks if the given table exists in the database """
        return sqlalchemy.inspect(self.engine).has_table(name)


    def create_database_if_not_exists(self, name: str) -> None:
        """ Creates a new database if not already exists """
        if not database_exists(self.engine.url):
            create_database(self.engine.url)


    def create_schema_if_not_exists(self, name: str) -> None:
        """ Creates a new Schema if not already exists """
        self._execute(f"CREATE SCHEMA IF NOT EXISTS {name}")


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