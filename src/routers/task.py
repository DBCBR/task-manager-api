from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models.task import TaskModel
from src.models.user import UserModel
from src.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from src.security.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks Management"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_input: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Cria uma nova tarefa e associa automaticamente ao usuário autenticado."""
    new_task = TaskModel(
        title=task_input.title,
        description=task_input.description,
        user_id=current_user.id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)  # Preenche o objeto com o ID gerado pelo Postgres
    return new_task

@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Lista apenas tarefas do usuário autenticado, com suporte a paginação."""
    tasks = (
        db.query(TaskModel)
        .filter(TaskModel.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return tasks

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
    """Atualiza uma tarefa do usuário autenticado."""
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.user_id == current_user.id,
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tarefa nao encontrada."
        )
    
    # Atualiza os campos da tarefa com os dados fornecidos
    if task_input.title is not None:
        task.title = task_input.title
    if task_input.description is not None:
        task.description = task_input.description
    if task_input.is_completed is not None:
        task.is_completed = task_input.is_completed

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