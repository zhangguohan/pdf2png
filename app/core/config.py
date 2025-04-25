import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "PDF to PNG Converter"
    
    # 临时文件目录
    TEMP_DIR: str = "temp"
    
    # 默认DPI设置
    DEFAULT_DPI: int = 200
    
    # API 密钥设置
    API_KEY: str = os.environ.get("API_KEY", "ADFeerer2343vdfFIOUKwefoijlsakfj98798")
    API_KEY_NAME: str = "x-api-key"
    
    class Config:
        env_file = ".env"

settings = Settings()

# 确保临时目录存在
os.makedirs(settings.TEMP_DIR, exist_ok=True)