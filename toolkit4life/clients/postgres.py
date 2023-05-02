# Standard imports
import uuid
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus as urlquote

# Third-party imports
from ._sqlalchemy import SQLAlchemy


class PostgresClient(SQLAlchemy):

    def __init__(self, host: str, port: str, username: str, password: str, database: str) -> None:
        """
            Creates and initializes a PostgreSQL engine instance that connects to the database

            Parameters:
                host (str): Host IP address
                port (str): Port number                
                username (str): Username for authentication/privileges
                password (str): Password for authentication
                database (str): Name of the database
        """
        super().__init__(engine = "postgresql", host = host, port = port, database = database, username = username, password = password)
        self.engine = create_engine(self.connection_string)


    def upsert_df(self, df: pd.DataFrame, table_name: str) -> None:
        """
            Implements the equivalent of pd.DataFrame.to_sql(..., if_exists='update') (which does not exist). Creates or updates the db records based on the dataframe records.

            Parameters:
                df (pd.DataFrame): Dataframe to upsert (NOTE: Primary keys of the destination 'table_name' must be equal to dataframe index and not present in the dataframe columns)
                table_name (str): Table name
                client (PostgresClient): Database client
            Returns:
                None
        """

        # Create a temporary table and insert the dataframe into it
        temp_table_name = f"temp_{uuid.uuid4().hex[:10]}"
        self._insert(df, temp_table_name, index = True)

        # Get the index and column names, and create the SQL text for them
        index_names = list(df.index.names)
        index_names_sql_txt = ", ".join([f'"{_}"' for _ in index_names])
        column_names = list(df.columns)
        headers_sql_txt = ", ".join([f'"{i}"' for i in index_names + column_names])  # SQL columns: idx1, idx2, col1, col2, ...

        # col1 = exluded.col1, col2=excluded.col2
        update_column_stmt = ", ".join([f'"{col}" = EXCLUDED."{col}"' for col in column_names])

        # Create a unique constraint on the index columns for the ON CONFILCT clause
        self.engine.execute(f"""
            ALTER TABLE "{table_name}" DROP CONSTRAINT IF EXISTS unique_constraint_{temp_table_name};
            ALTER TABLE "{table_name}" ADD CONSTRAINT unique_constraint_{temp_table_name} UNIQUE ({index_names_sql_txt});
        """)

        # Apply the upsert and remove the temporary table
        self.engine.execute(f"""
            INSERT INTO "{table_name}" ({headers_sql_txt}) 
            SELECT {headers_sql_txt} FROM "{temp_table_name}"
            ON CONFLICT ({index_names_sql_txt}) DO UPDATE 
            SET {update_column_stmt};
        """)
        self.engine.execute(f"DROP TABLE {temp_table_name}")


    @property
    def connection_string(self) -> str:
        """ Returns the connection string """
        return f"{self.engine}://{self.username}:%s@{self.host}:{self.port}/{self.database}" % urlquote(self.password)