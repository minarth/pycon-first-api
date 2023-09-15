from typing import Optional, Tuple
from typing_extensions import Annotated
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

from datamodel import Client, Product, ProductClient, ClientRepository, ProductRepository, ProductClientRepository

app = FastAPI()
client_repo = ClientRepository()
prod_repo = ProductRepository()
prod_client_repo = ProductClientRepository()


class ClientModel(BaseModel):
    first_name: Annotated[str, Query(min_length=3, pattern=r'^[a-zA-Z]+$')]
    last_name: Annotated[str, Query(min_length=3, pattern=r'^[a-zA-Z]+$')]


class TransferModel(BaseModel):
    from_uid: int   
    to_uid: int
    amount: float


@app.get("/")
async def root():
    return {"message": "Hello Bank"}


@app.get("/products")
async def product():
    return prod_repo.data


@app.get("/clients")
async def clients():
    return client_repo.data


@app.get("/clients/{client_uid}")
async def get_client(client_uid: int):
    if client_uid not in client_repo.data:
        raise HTTPException(status_code=404, detail="Client not found")
    return client_repo.data[client_uid]


@app.post("/clients")
async def create_client(client: ClientModel):
    return client_repo.add(None, Client(None, client.first_name, client.last_name))


@app.put("/clients/{client_uid}")
async def update_client(client_uid: int, client: ClientModel):
    # CLIENTS[client_id] = client
    return client


# TASK DO TRANSACTIONS
@app.get("/balance/{client_uid}/product/{product_uid}")
async def get_balance(client_uid: int, product_uid: int):
    if client_uid not in client_repo.data:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client = client_repo.data[client_uid]

    if product_uid not in prod_client_repo[client_uid]:
        raise HTTPException(status_code=404, detail=f"Client {client['name']}"  
                            "does not have product with ID: {product_id}")


@app.get("/balance/{product_client_uid}")
async def get_balance_specific(product_client_uid: int):
    if product_client_uid not in prod_client_repo.data:
        raise HTTPException(status_code=404, detail="Product with ID: {product_client_uid} not found")
    
    return prod_client_repo.data[product_client_uid]


@app.post("/send-money")
async def send_money(transfer: TransferModel):
    prod_client_repo[transfer.from_uid] -= transfer.amount
    prod_client_repo[transfer.to_uid] += transfer.amount

