from dataclasses import dataclass


@dataclass()
class Application:
    environment: str
    description: str
    title: str
    version: str
