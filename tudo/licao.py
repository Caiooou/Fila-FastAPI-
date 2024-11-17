from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

app = FastAPI()

class Cliente(BaseModel):
    nome: str
    tipo_atendimento: str 
    atendido: bool = False
    data_chegada: datetime = Field(default_factory=datetime.now)

fila: List[Cliente] = []

def atualizar_posicoes():
    for i, cliente in enumerate(fila):
        cliente.posicao = i


@app.get("/fila", response_model=List[Cliente])
async def get_fila():
    if not fila:
        return []
    return fila

@app.get("/fila/{id}", response_model=Cliente)
async def get_cliente(id: int):
    if id < 0 or id >= len(fila):
        raise HTTPException(status_code=404, detail="Cliente não encontrado na fila.")
    return fila[id]

@app.post("/fila", response_model=Cliente)
async def adicionar_cliente(nome: str, tipo_atendimento: str):
    if len(nome) > 20:
        raise HTTPException(status_code=400, detail="Nome não pode ter mais de 20 caracteres.")
    
    if tipo_atendimento not in ["N", "P"]:
        raise HTTPException(status_code=400, detail="Tipo de atendimento deve ser 'N' ou 'P'.")
    
    novo_cliente = Cliente(nome=nome, tipo_atendimento=tipo_atendimento, atendido=False)
    fila.append(novo_cliente)
    atualizar_posicoes()
    return novo_cliente

@app.put("/fila")
async def atualizar_fila():
    if not fila:
        raise HTTPException(status_code=404, detail="Não há clientes na fila.")
    
    if fila[0].atendido == False:
        fila[0].atendido = True  
    
    fila.pop(0)
    atualizar_posicoes()
    return {"message": "Fila atualizada com sucesso"}

@app.delete("/fila/{id}")
async def remover_cliente(id: int):
    if id < 0 or id >= len(fila):
        raise HTTPException(status_code=404, detail="Cliente não encontrado na fila.")
    
    del fila[id]
    atualizar_posicoes()
    return {"message": f"Cliente na posição {id} removido com sucesso."}
