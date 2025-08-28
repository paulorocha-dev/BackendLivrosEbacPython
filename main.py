# API de Livros

# GET - Buscar dados dos livros
# POST - Adicionar novos livros
# PUT - Atualizar dados dos livros 
# DELETE - Deletar informações dos livros

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets

app = FastAPI(
    title="API de Livros",
    description="Uma API simples para gerenciar uma coleção de livros.",
    version="1.0.0",
    contact={
        "name": "Paulo Henrique",
        "email": "paulo.souzarocha27@gmail.com"
    }
)

meu_usuario = "admin"
minha_senha = "admin123"

security = HTTPBasic()

meus_livros = {}

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, meu_usuario)
    is_password_correct = secrets.compare_digest(credentials.password, minha_senha)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/livros")
def get_livros(page: int = 1, limit: int = 10, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Parâmetros inválidos. 'page' e 'limit' devem ser maiores que 0.")
    
    if not meus_livros:
        return {"message": "Nenhum livro cadastrado."}
    
    start = (page - 1) * limit
    end = start + limit

    livros_paginados = [
        {"id": id_livro, "nome_livro": livro_data["nome_livro"], "autor_livro": livro_data["autor_livro"], "ano_livro": livro_data["ano_livro"]}
        for id_livro, livro_data in list(meus_livros.items())[start:end]
    ]

    return {
        "page": page,
        "limit": limit,
        "total_livros": len(meus_livros),
        "livros": livros_paginados
    }
    
@app.post("/adiciona")
def post_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if id_livro in meus_livros:
        raise HTTPException(status_code=400, detail="Livro já cadastrado.")
    else:
        meus_livros[id_livro] = livro.model_dump()
        return {"message": "Livro adicionado com sucesso."}
    
@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    meu_livro = meus_livros.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=400, detail="Livro não encontrado.")
    else:
        meus_livros[id_livro] = livro.model_dump()
        return {"message": "Livro atualizado com sucesso."}
    
@app.delete("/deletar/{id_livro}")
def delete_livros(id_livro: int, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if id_livro in meus_livros:
        del meus_livros[id_livro]
        return {"message": "Livro deletado com sucesso."}
    else:
        raise HTTPException(status_code=400, detail="Livro não encontrado.")