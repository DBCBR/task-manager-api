from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Manager API"
    PROJECT_VERSION: str = "1.0.0"
    
    # URL padrão caso o .env não exista
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/postgres"
    
    # Configurações do JWT
    SECRET_KEY: str = "sua_chave_secreta_super_segura"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Indica ao Pydantic para ler o arquivo .env na raiz do projeto
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
settings = Settings()