# Standard imports
from sqlalchemy import create_engine

# Third-party imports
from ._sqlalchemy import SQLAlchemy


class PostgresClient(SQLAlchemy):

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
        super().__init__(engine = "postgresql", host = host, port = port, database = database, username = username, password = password)
        self.engine = create_engine(self.connection_string)


    @property
    def connection_string(self) -> str:
        """ Returns the connection string """
        return f"{self.engine}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"