from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime, timezone

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# 1. Adicionamos o Enum de Prioridades
class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: TaskPriority = TaskPriority.LOW  # <-- Prioridade padrão na criação

class TaskCreate(TaskBase):
    @field_validator("due_date")
    @classmethod
    def validar_data_vencimento(cls, valor: Optional[datetime]) -> Optional[datetime]:
        if valor is not None:
            if valor.tzinfo is None:
                valor = valor.replace(tzinfo=timezone.utc)
            
            # Obtém o agora em UTC e subtrai 15 minutos de tolerância para cobrir delays de rede/digitação
            from datetime import timedelta
            limite_tolerancia = datetime.now(timezone.utc) - timedelta(minutes=15)
            
            if valor < limite_tolerancia:
                raise ValueError("A data de vencimento nao pode ser no passado (tolerancia de 15 min).")
        return valor

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    priority: Optional[TaskPriority] = None

    @field_validator("due_date")
    @classmethod
    def validar_data_vencimento(cls, valor: Optional[datetime]) -> Optional[datetime]:
        if valor is not None:
            if valor.tzinfo is None:
                valor = valor.replace(tzinfo=timezone.utc)
                
            from datetime import timedelta
            limite_tolerancia = datetime.now(timezone.utc) - timedelta(minutes=15)
            
            if valor < limite_tolerancia:
                raise ValueError("A data de vencimento nao pode ser no passado (tolerancia de 15 min).")
        return valor

class TaskResponse(TaskBase):
    id: int
    status: TaskStatus
    priority: TaskPriority  # <-- Retorna a prioridade no output
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class TaskStatsResponse(BaseModel):
    total_tasks: int
    pending_count: int
    in_progress_count: int
    completed_count: int
    completion_percentage: float