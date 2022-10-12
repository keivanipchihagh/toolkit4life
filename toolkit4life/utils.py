# Standard imports
import yaml

def read_config(project_name: str, path: str = "./config.yml") -> dict:
    """ Reads the config file and returns the configurations as a dictionary """
    with open(path, "r") as file:
        return yaml.safe_load(file)[project_name]