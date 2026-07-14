# Task Manager API

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Supported-2496ED?style=flat-square&logo=docker)](https://www.docker.com/)

Uma API RESTful robusta e segura para gerenciar tarefas com autenticação baseada em JWT. Desenvolvida com **FastAPI**, **SQLAlchemy** e **PostgreSQL**.

## 🎯 Características Principais

- ✅ **Autenticação JWT** - Autenticação segura com tokens JWT
- 📝 **Gerenciamento de Tarefas** - Criar, ler, atualizar e deletar tarefas
- 👤 **Gerenciamento de Usuários** - Registro e autenticação de usuários
- 🔒 **Isolamento de Dados** - Cada usuário só acessa suas próprias tarefas
- 🗂️ **ORM com SQLAlchemy** - Mapeamento objeto-relacional eficiente
- 🏥 **Health Check** - Endpoint de monitoramento da saúde da API
- 🐳 **Docker & Docker Compose** - Containerização e orquestração simplificada
- 📊 **Swagger/OpenAPI** - Documentação interativa automática
- 🧪 **Testes Automatizados** - Cobertura de testes com pytest

## 🚀 Início Rápido

### Pré-requisitos

- **Python 3.12+**
- **Docker & Docker Compose** (recomendado)
- **PostgreSQL 15** (se não usar Docker)

### Instalação com Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/DBCBR/task-manager-api.git
cd task-manager-api

# Inicie os serviços com Docker Compose
docker compose up -d

# A API estará disponível em: http://localhost:8000
# Swagger documentação: http://localhost:8000/docs
```

### Instalação Local

```bash
# Clone o repositório
git clone https://github.com/DBCBR/task-manager-api.git
cd task-manager-api

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Instale as dependências
poetry install

# Configure as variáveis de ambiente
copy .env.example .env

# Inicie o servidor
poetry run uvicorn src.main:app --reload
```

## 📋 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações da Aplicação
PROJECT_NAME=Task Manager API
PROJECT_VERSION=1.0.0

# Banco de Dados
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/taskdb

# Segurança
SECRET_KEY=sua_chave_secreta_super_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

⚠️ **IMPORTANTE**: Altere o `SECRET_KEY` em produção com uma chave segura e única!

### Migrações com Alembic

O projeto usa Alembic para versionar o schema do banco.

```bash
# Criar uma nova migração a partir dos modelos
poetry run alembic revision --autogenerate -m "descricao_da_mudanca"

# Aplicar as migrações
poetry run alembic upgrade head

# Reverter uma migração
poetry run alembic downgrade -1
```

## 📚 Estrutura do Projeto

```
task-manager-api/
├── src/
│   ├── __init__.py
│   ├── config.py                # Configurações e variáveis de ambiente
│   ├── database.py              # Configuração do banco de dados
│   ├── main.py                  # Aplicação principal FastAPI
│   ├── models/                  # Modelos SQLAlchemy
│   │   ├── task.py             # Modelo de Tarefas
│   │   └── user.py             # Modelo de Usuários
│   ├── routers/                 # Endpoints da API
│   │   ├── auth.py             # Rotas de autenticação
│   │   └── task.py             # Rotas de gerenciamento de tarefas
│   ├── schemas/                 # Schemas Pydantic (validação)
│   │   ├── task.py             # Schema de Tarefas
│   │   └── user.py             # Schema de Usuários
│   └── security/                # Autenticação e segurança
│       └── auth.py             # Lógica de autenticação JWT
├── tests/                       # Testes automatizados
│   ├── test_auth.py            # Testes de autenticação
│   └── test_tasks.py           # Testes de tarefas
├── Dockerfile                   # Configuração do container
├── docker-compose.yml          # Orquestração de containers
├── pyproject.toml              # Dependências do projeto
└── README.md                   # Este arquivo
```

## 🔌 Endpoints da API

### Autenticação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/auth/register` | Registrar novo usuário |
| `POST` | `/auth/login` | Fazer login e obter token JWT |

**Exemplo - Registrar Usuário:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario",
    "email": "usuario@example.com",
    "password": "senha123"
  }'
```

**Exemplo - Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario",
    "password": "senha123"
  }'
```

### Tarefas

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|:-------------:|
| `GET` | `/tasks` | Listar todas as tarefas do usuário | ✅ |
| `POST` | `/tasks` | Criar nova tarefa | ✅ |
| `GET` | `/tasks/{id}` | Obter detalhes de uma tarefa | ✅ |
| `PUT` | `/tasks/{id}` | Atualizar uma tarefa | ✅ |
| `DELETE` | `/tasks/{id}` | Deletar uma tarefa | ✅ |

**Exemplo - Criar Tarefa:**
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer SEU_TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implementar novo recurso",
    "description": "Adicionar autenticação OAuth2",
    "is_completed": false
  }'
```

### Infraestrutura

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/healthcheck` | Verificar saúde da API |

## 🧪 Testes

Execute os testes automatizados:

```bash
# Instale as dependências
poetry install

# Execute todos os testes
poetry run pytest

# Execute testes específicos
poetry run pytest tests/test_auth.py -v
poetry run pytest tests/test_tasks.py -v
```

## 🐳 Docker

### Build da Imagem

```bash
docker build -t task-manager-api:latest .
```

### Executar com Docker Compose

```bash
# Iniciar serviços
docker compose up -d

# Visualizar logs
docker compose logs -f web

# Parar serviços
docker compose down

# Remover volumes (dados)
docker compose down -v
```

### Acessar o Container

```bash
# Acessar shell do container da API
docker compose exec web sh

# Acessar shell do banco de dados
docker compose exec db psql -U postgres -d taskdb
```

## 🔐 Segurança

### Melhores Práticas Implementadas

- ✅ **Hash de Senhas** - Senhas são hasheadas com bcrypt
- ✅ **JWT Tokens** - Autenticação stateless com tokens JWT
- ✅ **Isolamento de Dados** - Usuários só acessam seus dados
- ✅ **Validação de Entrada** - Schemas Pydantic validam todos os dados
- ✅ **CORS** - Configuração segura de CORS

### Recomendações para Produção

1. **Altere o SECRET_KEY** - Use uma chave segura e única
2. **Configure HTTPS** - Use certificados SSL/TLS
3. **Variáveis de Ambiente** - Nunca comite credenciais no Git
4. **Database** - Use credenciais seguras e banco de dados gerenciado
5. **Rate Limiting** - Implemente limitação de taxa de requisições
6. **CORS** - Configure origens permitidas específicas

## 🛠️ Desenvolvimento

### Executar em Modo de Desenvolvimento

```bash
# Com hot-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Formatação e Linting

```bash
# Formatar código
black src/ tests/

# Verificar estilo
flake8 src/ tests/

# Verificar tipos
mypy src/
```

### Migrações de Banco de Dados

Usando Alembic:

```bash
# Gerar nova migração
alembic revision --autogenerate -m "Descrição da mudança"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1
```

## 📖 Documentação

A documentação interativa está disponível em:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🐛 Troubleshooting

### Erro de Conexão ao Banco de Dados

```bash
# Verificar se o PostgreSQL está rodando
docker compose logs db

# Verificar credenciais em .env
# Padrão: postgresql+psycopg2://postgres:postgres@db:5432/taskdb
```

### Porta 8000 já em uso

```bash
# Mudar porta no docker-compose.yml ou
docker compose up -d -p 8001:8000
```

### Erro ao Instalar Dependências

```bash
# Reinstalar dependências
poetry install --sync
```

## 📝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código

- Siga o estilo do projeto (Black para formatação)
- Adicione testes para novas funcionalidades
- Mantenha a cobertura de testes acima de 80%
- Escreva mensagens de commit claras

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**DBCBR**
- Email: dbcbr@hotmail.com
- GitHub: [@DBCBR](https://github.com/DBCBR)

## 🤝 Suporte

Encontrou um problema? Abra uma [Issue](https://github.com/DBCBR/task-manager-api/issues) no GitHub.

## 📚 Recursos Úteis

- [Documentação FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JWT Authentication](https://jwt.io/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

<div align="center">

**Made with ❤️ by DBCBR**

</div>
