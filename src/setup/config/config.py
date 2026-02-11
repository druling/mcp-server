from pydantic_settings import BaseSettings


class Config(BaseSettings):
    app_name: str = "Druling AI Server"
    debug: bool = False
    port: int = 8000

    internal_secret: str = ""

    log_level: str = "INFO"
    log_format: str = "standard"

    backend_url: str = "http://localhost:8000/internal/v1"
    timeout: int = 60
    max_retries: int = 3

    class Config:
        env_file = ".env"

config = Config()
