import pytest
from datetime import datetime, timedelta, timezone
from fastapi import status
from fastapi.testclient import TestClient
from src.main import app
from src.database import get_db
from src.models.user import UserModel
from src.models.task import TaskModel
from src.security.auth import create_access_token, get_password_hash

client = TestClient(app)

# --- FIXTURES DE BANCO DE DADOS E USUÁRIOS ---

@pytest.fixture(autouse=True)
def setup_db_users():
    """Cria os usuários de teste no banco de dados antes de rodar cada teste."""
    db = next(get_db())
    
    # Garante limpeza para evitar conflito de UNIQUE
    db.query(UserModel).filter(UserModel.username.in_(["usuario1", "usuario2"])).delete(synchronize_session=False)
    db.commit()

    # Cria o usuário 1
    user1 = UserModel(
        username="usuario1",
        email="user1@example.com",
        hashed_password=get_password_hash("senha_secreta_123")
    )
    # Cria o usuário 2
    user2 = UserModel(
        username="usuario2",
        email="user2@example.com",
        hashed_password=get_password_hash("senha_secreta_123")
    )
    
    db.add(user1)
    db.add(user2)
    db.commit()
    
    yield  # Executa o teste de fato
    
    # Limpa os dados de teste criados
    db = next(get_db())
    db.query(UserModel).filter(UserModel.username.in_(["usuario1", "usuario2"])).delete(synchronize_session=False)
    db.commit()


@pytest.fixture
def token_usuario_1():
    """Gera um token JWT válido para o usuário 1."""
    return create_access_token(data={"sub": "usuario1"})


@pytest.fixture
def token_usuario_2():
    """Gera um token JWT válido para o usuário 2."""
    return create_access_token(data={"sub": "usuario2"})


@pytest.fixture
def headers_user1(token_usuario_1):
    """Cria os cabeçalhos de autenticação para o usuário 1."""
    return {"Authorization": f"Bearer {token_usuario_1}"}


@pytest.fixture
def headers_user2(token_usuario_2):
    """Cria os cabeçalhos de autenticação para o usuário 2."""
    return {"Authorization": f"Bearer {token_usuario_2}"}


# --- NOVOS TESTES DE DATA DE VENCIMENTO (DUE DATE) e PRIORIDADE ---

def test_criar_tarefa_com_vencimento_futuro_e_prioridade(headers_user1):
    """Garante que é possível criar uma tarefa com prioridade alta e data no futuro."""
    amanha = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    payload = {
        "title": "Apresentar projeto de testes",
        "description": "Mostrar os testes funcionando para a Mimosa",
        "due_date": amanha,
        "priority": "high"
    }
    response = client.post("/tasks/", json=payload, headers=headers_user1)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["priority"] == "high"
    assert "due_date" in data
    assert data["due_date"] is not None


def test_criar_tarefa_com_data_no_passado_deve_retornar_422(headers_user1):
    """Garante que criar uma tarefa com data no passado (além da margem de 15m) falha."""
    ontem = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
    payload = {
        "title": "Tarefa do passado",
        "due_date": ontem
    }
    response = client.post("/tasks/", json=payload, headers=headers_user1)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert "data de vencimento nao pode ser no passado" in response.text


def test_criar_tarefa_com_data_limite_tolerancia_passa(headers_user1):
    """Garante que a tolerância de 15 minutos funciona (uma data de 5 minutos atrás passa)."""
    cinco_minutos_atras = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
    payload = {
        "title": "Tarefa com tolerância de tempo",
        "due_date": cinco_minutos_atras
    }
    response = client.post("/tasks/", json=payload, headers=headers_user1)
    
    assert response.status_code == status.HTTP_201_CREATED


# --- TESTES DO ENDPOINT DE ESTATÍSTICAS (STATS) ---

def test_dashboard_estatisticas_calculos_corretos(headers_user1):
    """Cria tarefas em diferentes estados e valida se a rota de estatísticas computa corretamente."""
    # 1. Cria tarefa 1 (Pendente)
    client.post("/tasks/", json={"title": "T1", "priority": "low"}, headers=headers_user1)
    
    # 2. Cria tarefa 2 (Em Progresso)
    res2 = client.post("/tasks/", json={"title": "T2", "priority": "medium"}, headers=headers_user1)
    task2_id = res2.json()["id"]
    client.put(f"/tasks/{task2_id}", json={"status": "in_progress"}, headers=headers_user1)

    # 3. Cria tarefa 3 (Concluída)
    res3 = client.post("/tasks/", json={"title": "T3", "priority": "high"}, headers=headers_user1)
    task3_id = res3.json()["id"]
    client.put(f"/tasks/{task3_id}", json={"status": "completed"}, headers=headers_user1)

    # 4. Busca as estatísticas do painel
    response = client.get("/tasks/stats", headers=headers_user1)
    assert response.status_code == status.HTTP_200_OK
    
    stats = response.json()
    assert stats["total_tasks"] == 3
    assert stats["pending_count"] == 1
    assert stats["in_progress_count"] == 1
    assert stats["completed_count"] == 1
    # 1 tarefa concluída de 3 no total = 33.33%
    assert stats["completion_percentage"] == 33.33


# --- TESTES LEGADOS ADAPTADOS PARA OS NOVOS SCHEMAS ---

def test_criar_tarefa_sucesso(headers_user1):
    """Garante que um usuário autenticado consegue criar uma tarefa padrão (prioridade low)."""
    payload = {
        "title": "Estudar Python e FastAPI",
        "description": "Praticar testes automatizados com Pytest"
    }
    response = client.post("/tasks/", json=payload, headers=headers_user1)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["status"] == "pending"
    assert data["priority"] == "low"  # Prioridade default


def test_atualizar_status_tarefa_sucesso(headers_user1):
    """Garante que é possível atualizar o status de uma tarefa para os tipos válidos."""
    payload = {"title": "Tarefa para Atualizar"}
    create_res = client.post("/tasks/", json=payload, headers=headers_user1)
    task_id = create_res.json()["id"]

    update_payload = {"status": "in_progress"}
    update_res = client.put(f"/tasks/{task_id}", json=update_payload, headers=headers_user1)
    
    assert update_res.status_code == status.HTTP_200_OK
    assert update_res.json()["status"] == "in_progress"


def test_filtrar_tarefas_por_status(headers_user1):
    """Garante que a API filtra as tarefas corretamente pelo parâmetro 'status'."""
    client.post("/tasks/", json={"title": "Pendente"}, headers=headers_user1)
    res = client.post("/tasks/", json={"title": "Completada"}, headers=headers_user1)
    task_id = res.json()["id"]
    client.put(f"/tasks/{task_id}", json={"status": "completed"}, headers=headers_user1)

    response = client.get("/tasks/?status=completed", headers=headers_user1)
    assert response.status_code == status.HTTP_200_OK
    tarefas = response.json()
    
    assert len(tarefas) >= 1
    for t in tarefas:
        assert t["status"] == "completed"


def test_busca_textual_por_titulo_ou_descricao(headers_user1):
    """Garante que o parâmetro de busca filtra por aproximação."""
    client.post("/tasks/", json={"title": "Comprar leite na padaria"}, headers=headers_user1)
    client.post("/tasks/", json={"title": "Fazer academia", "description": "Musculação pesada"}, headers=headers_user1)

    response = client.get("/tasks/?search=leite", headers=headers_user1)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert "leite" in response.json()[0]["title"]


def test_atualizar_status_invalido_deve_retornar_422(headers_user1):
    """Garante que enviar um status inválido retorna erro de validação."""
    payload = {"title": "Tarefa Nova"}
    create_res = client.post("/tasks/", json=payload, headers=headers_user1)
    task_id = create_res.json()["id"]

    bad_payload = {"status": "concluido_com_sucesso"}
    response = client.put(f"/tasks/{task_id}", json=bad_payload, headers=headers_user1)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_usuario_nao_pode_acessar_tarefa_de_outro_usuario(headers_user1, headers_user2):
    """Garante isolamento de dados: usuário 2 não pode ver tarefas do usuário 1."""
    payload = {"title": "Segredo do Usuário 1"}
    res = client.post("/tasks/", json=payload, headers=headers_user1)
    task_id = res.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=headers_user2)
    assert response.status_code == status.HTTP_404_NOT_FOUND