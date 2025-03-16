from typing import Any, Dict, Optional, Union

# https://pydantic-docs.helpmanual.io/usage/settings/
# Pydantic: Data validation and settings management using python type annotations.
from pydantic import PostgresDsn, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str
    POSTGRES_PORT: str
    API_VERSION_STR: str = "/api/v1"
    SECRET_KEY: str = "SG9wZWxpamsgZ2VicnVpa3QgZWVuIHN0dWRlbnQgZGl0IG9vaXQgbnV0dGlnLg=="
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10

    SQLALCHEMY_DATABASE_URI: Union[Optional[PostgresDsn], Optional[str]] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            port=int(values.get("POSTGRES_PORT")),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"{values.get('POSTGRES_DATABASE') or ''}",
        )

    class Config:
        case_sensitive = True
        # env_file = ".env"


settings = Settings()
