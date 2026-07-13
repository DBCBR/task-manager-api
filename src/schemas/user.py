from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr  # Valida se é um e-mail real (precisa do pacote pydantic[email])
    password: str = Field(..., min_length=6, description="Senha em texto limpo")

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str