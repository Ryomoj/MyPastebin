from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class ConfigBase(BaseSettings):

    model_config = SettingsConfigDict(
        env_file="settings/.env", env_file_encoding="utf-8", extra="ignore")

class DatabaseConfig(ConfigBase):

    model_config = SettingsConfigDict(env_prefix="DB_")

    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "postgres"
    PASS: str = "postgres"
    NAME: str = "pastebin"

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"


class Config(BaseSettings):
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)

    @classmethod
    def load(cls):
        return cls()

