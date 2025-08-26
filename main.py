# API de Livros

# GET - Buscar dados dos livros
# POST - Adicionar novos livros
# PUT - Atualizar dados dos livros 
# DELETE - Deletar informações dos livros

from fastapi import FastAPI, HTTPException

app = FastAPI()

meus_livros = {}

@app.get("/livros")
def get_livros():
    if not meus_livros:
        return {"message": "Nenhum livro cadastrado."}
    else:
        return {"livros": meus_livros}
    
@app.post("/adiciona")
def post_livros(id_livro: int, nome_livro: str, autor_livro: str, ano_livro: int):
    if id_livro in meus_livros:
        raise HTTPException(status_code=400, detail="Livro já cadastrado.")
    else:
        meus_livros[id_livro] = {
            "nome_livro": nome_livro,
            "autor_livro": autor_livro,
            "ano_livro": ano_livro
        }
        return {"message": "Livro adicionado com sucesso."}
    
@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, nome_livro: str, autor_livro: str, ano_livro: int):
    meu_livro = meus_livros.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    else:
        if nome_livro:
            meu_livro["nome_livro"] = nome_livro
        if autor_livro:
            meu_livro["autor_livro"] = autor_livro
        if ano_livro:
            meu_livro["ano_livro"] = ano_livro
        return {"message": "Livro atualizado com sucesso."}
    
@app.delete("/deletar/{id_livro}")
def delete_livros(id_livro: int):
    if id_livro in meus_livros:
        del meus_livros[id_livro]
        return {"message": "Livro deletado com sucesso."}
    else:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")