import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import Base, LivroDB, app, sessao_db
from fastapi.testclient import TestClient


DATABASE_URL_TEST = "sqlite:///:memory:"


engine = create_engine(
    DATABASE_URL_TEST,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool   # <<< IMPORTANTE
)


TestingSessionLocal = sessionmaker(bind=engine)


Base.metadata.create_all(bind=engine)



# Override da sessão da API
def override_sessao_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[sessao_db] = override_sessao_db


client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_redis(mocker):
    mock_redis_client = mocker.patch("main.redis_client", autospec=True)
    mock_redis_client.get.return_value = None


@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_get_books(db):

    # Insere 10 livros no banco de teste
    for i in range(10):
        livro = LivroDB(
            nome_livro="Harry Potter e a Pedra Filosofal",
            autor_livro="J.K.",
            ano_livro=1999
        )
        db.add(livro)

    db.commit()

    response = client.get("/livros", auth=("admin", "admin123"))

    assert response.status_code == 200

    data = response.json()

    assert "livros" in data
    assert len(data["livros"]) == 10

    assert data["livros"][0]["nome_livro"] == "Harry Potter e a Pedra Filosofal"
    assert data["livros"][0]["autor_livro"] == "J.K."
    assert data["livros"][0]["ano_livro"] == 1999
