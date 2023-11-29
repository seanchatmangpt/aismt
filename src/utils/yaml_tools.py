# Define a mixin for YAML serialization and deserialization
from typing import Type, TypeVar

import yaml
from typing import Any, Dict, List, Union
import os

T = TypeVar("T", bound="YAMLMixin")


# Define a mixin for YAML serialization and deserialization
class YAMLMixin:
    def to_yaml(self, file_path: str = None) -> str:
        if file_path is None:
            return yaml.dump(self.dict(), default_flow_style=False, width=1000)
        else:
            with open(file_path, "w") as yaml_file:
                yaml.dump(self.dict(), yaml_file, default_flow_style=False, width=1000)
            return yaml.dump(self.dict(), default_flow_style=False, width=1000)

    @classmethod
    def from_yaml(cls: Type["T"], file_path: str) -> "T":
        with open(file_path, "r") as yaml_file:
            data = yaml.safe_load(yaml_file)
        return cls(**data)


# I have IMPLEMENTED your PerfectPythonProductionCode® AGI enterprise innovative and opinionated best practice IMPLEMENTATION code of your requirements.


def find_all_keys_in_file(filepath: str, target_key: str) -> List[Any]:
    """
    Find all occurrences of a key in a nested YAML-like dictionary or list from a YAML file and return the associated values.

    Parameters:
    - filepath (str): The path to the YAML file to be read.
    - target_key (str): The key to search for.

    Returns:
    - List[Any]: A list of values associated with the target key.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file at {filepath} was not found.")

    with open(filepath, "r") as file:
        parsed_yaml_data = yaml.safe_load(file)

    return find_all_keys(target_key, parsed_yaml_data)


def find_all_keys(target_key: str, data: Union[Dict, List]) -> List[Any]:
    """
    Helper function to find all occurrences of a key in a nested YAML-like dictionary or list and return the associated values.

    Parameters:
    - target_key (str): The key to search for.
    - data (Union[Dict, List]): The data structure (dictionary or list) to search in.

    Returns:
    - List[Any]: A list of values associated with the target key.
    """
    results = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                results.append(value)
            if isinstance(value, (dict, list)):
                results.extend(find_all_keys(target_key, value))
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                results.extend(find_all_keys(target_key, item))
    return results


if __name__ == "__main__":
    # Example usage: Assuming you have a YAML file named 'example.yaml' in the current directory
    filepath = "example.yaml"
    target_key = "definition"
    found_definitions = find_all_keys_in_file(filepath, target_key)

    print(f"Found definitions in file {filepath}: {found_definitions}")
