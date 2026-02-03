import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from main import Base, sessao_db, app


# Banco exclusivo para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Cria as tabelas IMEDIATAMENTE
Base.metadata.create_all(bind=engine)


# Override do DB
def override_sessao_db():

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[sessao_db] = override_sessao_db


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
