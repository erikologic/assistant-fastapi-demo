from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    auth0_domain: str
    auth0_api_audience: str
    auth0_issuer: str
    auth0_algorithms: str
    slack_token: str

    model_config = ConfigDict(env_file=".env", extra="allow")


@lru_cache()
def get_settings():
    return Settings()
