from fastapi import FastAPI, Depends  # <-- Adicione o Depends aqui nos imports
from src.config import settings
from src.database import Base, engine 
from src.routers import task, auth

# Importe o esquema de segurança para o arquivo principal
from src.security.auth import oauth2_scheme  # <-- ADICIONE ESTE IMPORT

# ... configuração dos modelos e tabelas ...
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

app.include_router(auth.router)  
app.include_router(task.router)

@app.get("/healthcheck", tags=["Infrastructure"])
# Adicionamos aqui apenas para o Swagger "saber" que o esquema existe na API inteira, 
# mas usando None para não bloquear a resposta do monitoramento.
def health_check(token: str = Depends(oauth2_scheme)):  
    """Rota para sistemas de monitoramento testarem se a API está online."""
    return {"status": "healthy", "version": settings.PROJECT_VERSION}