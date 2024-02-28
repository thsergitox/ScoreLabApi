# import os
from dotenv import load_dotenv

env_path = '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_NAME: str = "ScoreLab API"
    # DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:port/name")


settings = Settings()
