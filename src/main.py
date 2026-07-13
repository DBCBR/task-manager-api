from fastapi import FastAPI
from src.config import settings
from src.routers import task  # Importa o módulo das rotas

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

# Acopla as rotas de tarefas à aplicação principal
app.include_router(task.router)

@app.get("/healthcheck", tags=["Infrastructure"])
def health_check():
    """Rota para sistemas de monitoramento testarem se a API está online."""
    return {"status": "healthy", "version": settings.PROJECT_VERSION}