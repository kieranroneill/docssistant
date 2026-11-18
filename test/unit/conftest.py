from dotenv import load_dotenv


def pytest_sessionstart() -> None:
    load_dotenv(".env.test")
