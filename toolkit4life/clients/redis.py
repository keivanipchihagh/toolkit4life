# Standard imports
import redis
from pandas import DataFrame


class RedisClient():

    def __init__(self, host: str, port: str, password: str = None, db: int = 0, fresh_start: bool = False) -> None:
        """
            Initialized the Redis cache database instance and redis engine

            Parameters:
                host (str): the host of the redis server
                port (str): the port of the redis server                
                password (str): The password for the redis database
                db (int): The database to use. defaults to 0 if not spesified
                fresh_start (str): Whether to clear the redis database. Setting the argument to True can result in data-loss!
        """

        # Initialize the redis engine
        self.engine = redis.Redis(
            connection_pool = redis.ConnectionPool(
                host = host,
                port = port,
                password = password,
                decode_responses = True,    # Stringify the values
                db = db                     # Dedicated database
            )
        )

        # Test connection and throw error if connection was not successful
        if self.test_connection() is False:
            raise Exception("Could not connect to the redis database")

        # Clear the database if fresh_start is set to true
        if fresh_start:
            self.engine.flushdb()


    def test_connection(self) -> None:
        """ Tests connection to the redis cache """
        self.engine.ping()


    def close(self) -> None:
        """ Closes the redis connection """
        self.engine.close()


    def get_keys_from_pattern(self, pattern: str) -> list:
        """ Returns keys that match the given pattern """
        return self.engine.keys(pattern)


    def get_keys_all(self) -> list:
        """ Returns all the keys """
        return self.engine.keys("*")


    def get_values_from_list(self, keys: list) -> list:
        """ Returns the values for the given list of keys """
        with self.engine.pipeline() as pipe:
            for key in keys:
                pipe.hgetall(key)
            return [records for records in pipe.execute()]


    def get_values_from_pattern(self, pattern: str) -> list:
        """ Returns the values for the given pattern """
        return self.get_values_from_list(self.get_keys_from_pattern(pattern))


    def get_values_all(self) -> list:
        """ Returns all the values """
        return self.get_values_from_list(self.get_keys_all())


    def get_value_from_key(self, key: str) -> dict:
        """ Returns the value for the given key """
        return self.engine.hgetall(key)


    def get_dict_all(self) -> dict:
        """ Returns the keys and values as a dictionary """
        return dict(zip(self.get_keys_all(), self.get_values_all()))


    def get_dict_from_list(self, keys = list) -> dict:
        """ Returns the keys and values as a dictionary """
        return dict(zip(keys, self.get_values_from_list(keys)))


    def get_dict_from_pattern(self, pattern: str) -> dict:
        """ Returns the keys and values as a dictionary """
        keys = self.get_keys_from_pattern(pattern)
        return dict(zip(keys, self.get_values_from_list(keys)))


    def delete_values_from_list(self, keys: list) -> None:
        """ Deletes the given list of keys """
        with self.engine.pipeline() as pipe:
            for key in keys:
                pipe.delete(key)
            pipe.execute()


    def delete_key(self, key: str) -> None:
        """ Deletes the given key """
        self.engine.delete(key)


    def insert_key_value(self, key: str, value: dict) -> None:
        """ Inserts the given key and value """
        self.engine.hmset(key, value)


    def inset_dataframe(self, df: DataFrame, key_column: str = "id") -> None:
        """ Inserts a dataframe to the redis database with the key_column as the key """
        with self.engine.pipeline() as pipe:
            for _, row in df.iterrows():
                pipe.hmset(row[key_column], dict(row))
            pipe.execute()