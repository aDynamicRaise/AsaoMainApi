from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
import pytz

# Указываем часовой пояс Москвы
# *Использование: 
# *from config import msk_timezone
# *date_variable = datetime.now(msk_timezone)
msk_timezone = pytz.timezone("Europe/Moscow")

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class ApiPrefix(BaseModel):
    prefix: str = "/api"
    users:  str = "/users"
    stats: str = "/statistics"
    collecting: str = "/collecting"
    forecast: str = "/forecast"
    

class SecretsConfig(BaseModel):
    JWT_SECRET_KEY: str
    TEMP_JWT_SECRET_KEY: str
    login_mail: str
    password_mail: str
    

class DatabaseConfig(BaseSettings):
    url_migrations: PostgresDsn
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False

    naming_convention: dict[str, str] = {
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    secrets: SecretsConfig
    

settings = Settings()