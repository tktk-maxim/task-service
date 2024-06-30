import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    test_db_user: str = None
    test_db_password: str = None
    test_db_host: str = None
    test_db_port: str = None
    test_db_name: str = None

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')


settings = Settings()


def get_db_url(test: bool = False) -> str:
    if test:
        return (f'postgres://{settings.test_db_user}:{settings.test_db_password}'
                f'@{settings.test_db_host}:{settings.test_db_port}/{settings.test_db_name}')
    return (f'postgres://{settings.db_user}:{settings.db_password}'
            f'@{settings.db_host}:{settings.db_port}/{settings.db_name}')
