from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# --- IMPORTANTE: Seus modelos e configurações do projeto ---
from src.database import Base
from src.config import settings
from src.models.user import UserModel
from src.models.task import TaskModel

# Configuração de logs do Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Define o target_metadata para o autogenerate ler seus modelos
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Roda migrações em modo offline."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Roda migrações em modo online (conectando ao banco real)."""
    db_url = str(settings.DATABASE_URL)
    
    # Injeta a URL do banco de dados das configurações na raiz do Alembic
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = db_url
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()