import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, app
from fastapi.testclient import TestClient

DATABASE_URL = "sqlite:///./test_db.sqlite"  # arquivo temporário para CI

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)  # cria tabelas
    yield
    # opcional: apagar o arquivo no final
    import os
    os.remove("./test_db.sqlite")

@pytest.fixture()
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture()
def client(db_session):
    # Override o dependency do FastAPI
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
