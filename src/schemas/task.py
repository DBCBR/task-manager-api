from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Schema Base
class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Título da tarefa")
    description: Optional[str] = Field(None, max_length=500, description="Descrição detalhada")

# Schema de Entrada (Criação) - Verifique o nome exato da classe abaixo:
class TaskCreate(TaskBase):
    pass

# Schema de Atualização - Verifique o nome exato da classe abaixo:
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_completed: Optional[bool] = None

# Schema de Saída - Verifique o nome exato da classe abaixo:
class TaskResponse(TaskBase):
    id: int
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}