import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


# Localiza a raiz do projeto
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Carrega as variáveis do arquivo .env
load_dotenv(PROJECT_ROOT / ".env")


def criar_engine():
    """Cria e retorna uma conexão com o PostgreSQL."""

    url = URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME"),
    )

    return create_engine(url, pool_pre_ping=True)
