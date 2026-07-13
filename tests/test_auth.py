from src.security.auth import get_password_hash, verify_password, create_access_token
from jose import jwt
from src.config import settings

def test_password_hashing_and_verification():
    """Garante que a senha é criptografada e validada corretamente."""
    senha_original = "secret123"
    hash_da_senha = get_password_hash(senha_original)
    
    # 1. A senha original NÃO pode ser igual ao hash
    assert hash_da_senha != senha_original
    
    # 2. A verificação com a senha correta deve retornar True
    assert verify_password(senha_original, hash_da_senha) is True
    
    # 3. A verificação com uma senha errada deve retornar False
    assert verify_password("senha_errada", hash_da_senha) is False

def test_jwt_token_generation_and_decoding():
    """Garante que o token JWT é gerado com os dados corretos do usuário."""
    dados_usuario = {"sub": "user_teste_123"}
    token = create_access_token(data=dados_usuario)
    
    # Decodifica o token usando a nossa chave secreta para checar a integridade
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
    assert payload.get("sub") == "user_teste_123"
    assert "exp" in payload  # O token precisa ter uma data de expiração