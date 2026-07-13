from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models.task import TaskModel
from src.schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks Management"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_input: TaskCreate, db: Session = Depends(get_db)):
    """Cria uma nova tarefa no banco de dados com dados validados pelo Pydantic."""
    new_task = TaskModel(
        title=task_input.title,
        description=task_input.description
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)  # Preenche o objeto com o ID gerado pelo Postgres
    return new_task

@router.get("/", response_model=List[TaskResponse])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista as tarefas com suporte a paginação corporativa basica (skip e limit)."""
    tasks = db.query(TaskModel).offset(skip).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    """Busca uma tarefa específica pelo ID. Retorna 404 se não for encontrada."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task com id {task_id} não encontrada."
        )
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_input: TaskUpdate, db: Session = Depends(get_db)):
    """Atualiza uma tarefa existente com os dados fornecidos. Retorna 404 se não for encontrada."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task com id {task_id} não encontrada."
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
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Deleta uma tarefa específica pelo ID. Retorna 404 se não for encontrada."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task com id {task_id} não encontrada."
        )
    
    db.delete(task)
    db.commit()
    return None