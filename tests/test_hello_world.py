from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_hello_world():
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Olá, Mundo! A API de Livros está funcionando."}