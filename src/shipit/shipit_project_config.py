import tempfile
from datetime import datetime

from pydantic import BaseModel
from typing import List, Dict, Optional
from pathlib import Path

from utils.yaml_tools import YAMLMixin


# Using the YAMLMixin class as defined earlier
class ShipitProjectConfig(YAMLMixin, BaseModel):
    project_name: str
    description: Optional[str] = None
    ship_date: Optional[str] = None
    directory: Optional[str] = None
    version_control: Optional[Dict[str, str]] = None
    dependencies: List[str] = []
    configuration: Dict[str, str] = {}

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True

    @property
    def config_file(self) -> str:
        return (
            self.directory + "/shipit_project.yaml"
            if self.directory
            else str(Path("shipit_project.yaml"))
        )

    def save(self):
        self.to_yaml(file_path=str(self.config_file))

    @classmethod
    def load(cls, file_path: Optional[str] = None):
        file_path = file_path or Path("shipit_project.yaml")

        if Path(file_path).exists():
            cls.from_yaml(str(file_path))


def main():
    # get a temp directory
    temp_dir = tempfile.TemporaryDirectory()

    # Usage Example
    project_config = ShipitProjectConfig(
        project_name="My New Project",
        description="Description here",
        ship_date="2023-12-31",
        directory=str(Path(temp_dir.name)),
    )

    # Save to YAML file
    project_config.save()

    # Load from YAML file
    loaded_config = ShipitProjectConfig.load(
        Path(f"{temp_dir.name}/shipit_project.yaml")
    )
    # print(loaded_config)


if __name__ == "__main__":
    main()
