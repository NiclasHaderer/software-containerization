import os

from pydantic import BaseSettings, Field


class _Settings(BaseSettings):
    db_folder = Field(f"{os.getcwd()}/database/", env="DB_FOLDER")
    production = Field(False, env="PRODUCTION")
    spoof_user = Field(True, env="SPOOF_USER")


SETTINGS = _Settings()
