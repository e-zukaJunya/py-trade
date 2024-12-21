from dataclasses import dataclass


@dataclass
class Environments:
    """環境変数"""

    LOG_LEVEL: str = None
    SYS_CODE: str = None
    ENV: str = None
    DB_SECRET_ID: str = None
    OUTPUT_BUCKET: str = None
    DB_HOST: str = None
    DB_PORT: str = None
    DB_SERVICE_NAME: str = None
    DB_USER: str = None
    DB_PASSWORD: str = None
