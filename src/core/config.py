from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.logger import setup_logging


class Settings(BaseSettings):
    project_name: str = 'Library'
    project_description: str = 'test task for EM'
    project_url: str = Field('', env="PROJECT_URL")

    db_name: str = Field('library', env='DB_NAME')
    db_user: str = Field('user', env='DB_USER')
    db_host: str = Field('localhost', env='DB_HOST')
    db_port: str = Field('5432', env='DB_PORT')
    db_password: str = Field('pass', env='DB_PASSWORD')
    db_echo: bool = True

    borrow_period: int = 21

    @property
    def database_url(self):
        return f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='allow',
    )


settings = Settings()

logger = setup_logging('auth')
