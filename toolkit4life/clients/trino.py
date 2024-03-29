# Standard imports
from sqlalchemy import create_engine
from urllib.parse import quote_plus as urlquote

# Third-party imports
from ._sqlalchemy import SQLAlchemy


class TrinoClient(SQLAlchemy):

    def __init__(self, host: str, port: str, catalog: str, schema: str, username: str, password: str, connect_args: dict = {}) -> None:
        """
            Creates and initializes a PostgreSQL engine instance that connects to the database

            Parameters:
                host (str): Host IP address
                port (str): Port number
                catalog (str): Database name
                schema (str): Schema name
                username (str): Username for authentication/privileges
                password (str): Password for authentication
                connect_args (dict): Extrac arguments for the connection to be made
        """
        super().__init__(engine = "trino", host = host, port = port, database = catalog, username = username, password = password)
        self.schema = schema

        self.engine = create_engine(self.connection_string, connect_args = connect_args)


    @property
    def connection_string(self) -> str:
        """ Returns the connection string """
        return f"{self.engine}://{self.username}:%s@{self.host}:{self.port}/{self.database}/{self.schema}" % urlquote(self.password)