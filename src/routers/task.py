from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from src.database import get_db
from src.models.task import TaskModel
from src.models.user import UserModel
from src.schemas.task import TaskCreate, TaskUpdate,TaskResponse,TaskStatus,TaskPriority,TaskStatsResponse
from src.security.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks Management"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_input: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    new_task = TaskModel(
        title=task_input.title,
        description=task_input.description,
        due_date=task_input.due_date,
        priority=task_input.priority.value,  # <-- Salvando a prioridade!
        user_id=current_user.id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[TaskStatus] = Query(None, alias="status"),
    priority_filter: Optional[TaskPriority] = Query(None, alias="priority", description="Filtrar por prioridade"), # <-- Novo parâmetro!
    search: Optional[str] = Query(None, description="Buscar termo no título ou descrição"),
    overdue: Optional[bool] = Query(None, description="Filtrar apenas tarefas atrasadas"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    query = db.query(TaskModel).filter(TaskModel.user_id == current_user.id)

    if status_filter:
        query = query.filter(TaskModel.status == status_filter.value)

    if priority_filter:
        query = query.filter(TaskModel.priority == priority_filter.value)  # <-- Filtro de prioridade!

    if search:
        query = query.filter(
            TaskModel.title.ilike(f"%{search}%") | 
            TaskModel.description.ilike(f"%{search}%")
        )

    if overdue is True:
        agora = datetime.now(timezone.utc)
        query = query.filter(
            TaskModel.due_date < agora,
            TaskModel.status != TaskStatus.COMPLETED.value
        )

    tasks = query.offset(skip).limit(limit).all()
    return tasks

@router.get("/stats", response_model=TaskStatsResponse)
def get_task_stats(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Retorna estatísticas e métricas de desempenho das tarefas do usuário logado."""
    # 1. Total de tarefas do usuário
    total = db.query(TaskModel).filter(TaskModel.user_id == current_user.id).count()

    # 2. Agrupamento por status para obter a contagem de cada um de uma só vez
    results = db.query(
        TaskModel.status, 
        func.count(TaskModel.id)
    ).filter(
        TaskModel.user_id == current_user.id
    ).group_by(TaskModel.status).all()

    # Mapeia os resultados da query em um dicionário de contagens
    # Exemplo de saída do BD: [('pending', 3), ('completed', 5)]
    counts = {status: count for status, count in results}

    pending = counts.get("pending", 0)
    in_progress = counts.get("in_progress", 0)
    completed = counts.get("completed", 0)

    # 3. Calcula o percentual de conclusão de forma segura contra divisão por zero
    completion_percentage = 0.0
    if total > 0:
        completion_percentage = (completed / total) * 100

    return {
        "total_tasks": total,
        "pending_count": pending,
        "in_progress_count": in_progress,
        "completed_count": completed,
        "completion_percentage": round(completion_percentage, 2)  # Arredondado para duas casas decimais
    }

@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Busca uma tarefa do usuário autenticado pelo ID."""
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.user_id == current_user.id,
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tarefa nao encontrada ou sem permissao para acesso."
        )
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_input: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.user_id == current_user.id,
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tarefa nao encontrada."
        )
    
    if task_input.title is not None:
        task.title = task_input.title
    if task_input.description is not None:
        task.description = task_input.description
    if task_input.status is not None:
        task.status = task_input.status.value
    if task_input.due_date is not None:
        task.due_date = task_input.due_date
    if task_input.priority is not None:
        task.priority = task_input.priority.value  # <-- Atualizando a prioridade!

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Deleta uma tarefa do usuário autenticado."""
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.user_id == current_user.id,
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tarefa nao encontrada."
        )
    
    db.delete(task)
    db.commit()
    return None