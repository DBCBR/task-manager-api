from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Manager API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Configurações do Banco de Dados
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/taskdb"
    
    # Segurança
    SECRET_KEY: str = "sua_chave_secreta_super_segura_aqui"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Padrão V2 explícito para ler arquivos .env se existirem, ignorando se não achar
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignora variáveis extras do ambiente que não mapeamos

settings = Settings()