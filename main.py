from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing_extensions import Annotated


from datamodel import ClientRepository, ProductRepository, ProductClientRepository
from datamodel import Client, Product

app = FastAPI()

clients_repo = ClientRepository()
product_repo = ProductRepository()
product_client_repo = ProductClientRepository()


@app.get("/status")
async def root():
    import requests

    url = "http://127.0.0.1:8000/status"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return {"message": response.text}


@app.get("/clients")
async def get_clients():
    return clients_repo.data


# Task 1a - prepare get products endpoint.
@app.get("/products")
async def get_products():
    return product_repo.data


@app.get("/clients/{id_client}")
async def get_client(id_client: int):
    if id_client not in clients_repo.data:
        raise HTTPException(404, f"Client with `{id_client}` ID not found")
    return clients_repo.data[id_client]

# Task1b: GET Product specific data
# Bonus: GET Client by name

@app.get("/products/{id_product}")
async def get_product(id_product: int):
    if id_product not in product_repo.data:
        raise HTTPException(404, f"Product with `{id_product}` ID not found")
    return product_repo.data[id_product]


@app.get("/find-clients")
async def find_clients(query: str):
    found = []
    for client in clients_repo.data.values():
        if query in (client.first_name, client.last_name):
            found.append(client)
    
    return {"clients_found": found}


# get balance by account id

@app.get("/account/{id_account}")
async def get_account(id_account: int):
    if id_account not in product_client_repo.data:
        raise HTTPException(404, f"Account with `{id_account}` ID not found")
    return product_client_repo.data[id_account]


# get balance client id a product id
@app.get("/clients/{id_client}/products/{id_product}/balance")
async def get_account_balance(id_client: int, id_product: int):
    
    accounts = {}
    for id_acc, account in product_client_repo.data.items():
        if account.client_uid == id_client and account.product_uid == id_product:
            accounts[id_acc] = account.params

    return accounts


class ProductModel(BaseModel):
    name: str


@app.post("/products")
async def create_product(product: ProductModel):
    created_product = product_repo.add(None, Product(None, product.name))
    return created_product

class ClientModel(BaseModel):
    first_name: Annotated[str, Query(min_length=3, pattern=r"^[a-zA-Z]+$")]
    last_name: Annotated[str, Query(min_length=3, pattern=r"^[a-zA-Z]+$")]


# CREATE new Client
@app.post("/clients")
async def create_client(client: ClientModel):
    return clients_repo.add(None, Client(None, client.first_name, client.last_name))



@app.delete("/clients/{id_client}")
async def delete_client(id_client: int):
    if id_client not in clients_repo.data:
        raise HTTPException(404, f"Client with `{id_client}` ID not found")
    del clients_repo.data[id_client]

    return {"status": "OK"}
