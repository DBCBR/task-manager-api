from fastapi import FastAPI
from src.config import settings
from src.database import Base, engine 
from src.routers import task, auth

# Importante: importar os modelos antes do create_all para mapear as tabelas
from src.models.task import TaskModel
from src.models.user import UserModel

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

app.include_router(auth.router)  
app.include_router(task.router)

@app.get("/healthcheck", tags=["Infrastructure"])
def health_check():
    """Rota para sistemas de monitoramento testarem se a API está online."""
    return {"status": "healthy", "version": settings.PROJECT_VERSION}