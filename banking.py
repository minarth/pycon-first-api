from typing import Optional, Tuple
from typing_extensions import Annotated
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

from datamodel import Client, ClientRepository, ProductRepository, ProductClientRepository

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


@app.delete("/clients/{client_uid}")
async def delete_client(client_uid: int):
    if client_uid not in client_repo.data:
        raise HTTPException(status_code=404, detail="Client not found")
    
    del client_repo.data[client_uid]
    return {"status": "OK"}
    

# TASK DO TRANSACTIONS
@app.get("/balance/{client_uid}/product/{product_uid}")
async def get_balance(client_uid: int, product_uid: int):
    if client_uid not in client_repo.data:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client = client_repo.data[client_uid]

    if product_uid not in prod_repo.data:
        raise HTTPException(status_code=404, 
                detail=f"Product {product_uid} not found")

    # let's find the products
    found_products = {}

    for acc_num, prod_client in prod_client_repo.data.items():
        if prod_client.client_uid == client_uid \
            and prod_client.product_uid == product_uid:
            found_products[acc_num] = prod_client
        
    return found_products


@app.get("/balance/{product_client_uid}")
async def get_balance_specific(product_client_uid: int):
    if product_client_uid not in prod_client_repo.data:
        raise HTTPException(status_code=404, detail="Product with ID: {product_client_uid} not found")
    
    return {"balance": prod_client_repo.data[product_client_uid].params["balance"]}


@app.post("/send-money")
async def send_money(transfer: TransferModel):
    if transfer.from_uid not in prod_client_repo.data:
        raise HTTPException(status_code=404, detail=f"Transfer entity with ID: {transfer.from_uid} not found")

    if transfer.to_uid not in prod_client_repo.data:
        raise HTTPException(status_code=404, detail=f"Transfer entity with ID: {transfer.to_uid} not found")
    

    prod_client_repo.data[transfer.from_uid].params["balance"] -= transfer.amount
    prod_client_repo.data[transfer.to_uid].params["balance"] += transfer.amount

    return {"status": "OK"}

