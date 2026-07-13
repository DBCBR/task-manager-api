from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
import bcrypt  # <-- Mudamos para o bcrypt direto
from src.config import settings
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_password_hash(password: str) -> str:
    """Transforma a senha limpa em um Hash seguro de forma nativa."""
    # Converte a string para bytes, gera o salt e faz o hash
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')  # Retorna como string para salvar no banco

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto limpo bate com o hash salvo."""
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Gera o Token JWT (o crachá digital do usuário)."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt