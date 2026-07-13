from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from src.database import get_db
from src.models.user import UserModel
from src.schemas.user import UserCreate, UserResponse, Token
from src.security.auth import get_password_hash, verify_password, create_access_token, oauth2_scheme
from src.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_input: UserCreate, db: Session = Depends(get_db)):
    """Cadastra um novo usuário no sistema com senha criptografada."""
    # Verifica se o username já existe
    existing_username = db.query(UserModel).filter(UserModel.username == user_input.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este nome de usuário já está sendo usado."
        )
        
    # Verifica se o e-mail já existe
    existing_email = db.query(UserModel).filter(UserModel.email == user_input.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado."
        )

    # Cria o usuário aplicando o hash na senha
    new_user = UserModel(
        username=user_input.username,
        email=user_input.email,
        hashed_password=get_password_hash(user_input.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Autentica o usuário e retorna o Token JWT (Crachá Digital)."""
    # Busca o usuário pelo username (o form_data traz o login no campo 'username')
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    
    # Se não achar ou a senha não bater com o hash, retorna 401 (Não Autorizado)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gera o Token JWT contendo o username do usuário no "sub" (subject)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}