from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    PROJECT_NAME: str = 'MultiDB with pandasAI'
    # General
    API_VERSION: str = "/api/v1"

    class Config:
        env_file = ".env"
        from_attributes = True

settings = Settings()
