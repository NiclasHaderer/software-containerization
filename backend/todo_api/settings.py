from __future__ import annotations

from pydantic import BaseSettings, Field


class _Settings(BaseSettings):
    production = Field(False, env="PRODUCTION")
    db_user = Field("todo_user", env="DB_USER")
    db_password = Field("super_secret", env="DB_PASSWORD")
    db_driver = Field("postgresql+aiopg", env="DB_DRIVER")
    db_uri = Field("127.0.0.1:5432", env="DB_URI")
    single_node = Field(True, env="SINGLE_NODE")

    @property
    def db_connection(self) -> str:
        return (
            f"{self.db_driver}://{self.db_user}:{self.db_password}@{self.db_uri}/todo"
        )


SETTINGS = _Settings()
print(SETTINGS)
