import tomllib
from pathlib import Path


def get_version(pyproject_path: Path) -> str:
    """
    Gets the version from the pyproject.toml file.

    Args:
        pyproject_path (Path): The path to the pyproject.toml file.

    Returns:
        str: The version of the application.
    """
    with pyproject_path.open("rb") as pyproject:
        version = tomllib.load(pyproject)["project"]["version"]

    return version
