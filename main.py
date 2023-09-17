from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from datamodel import Client, Product, \
    ClientRepository, ProductRepository, ProductClientRepository

app = FastAPI()

client_repo = ClientRepository()
prod_repo = ProductRepository()
prod_client_repo = ProductClientRepository()

@app.get("/status")
async def root():
    return {"message": "OK"}


@app.get("/clients")
async def get_clients():
    return client_repo.data


@app.get("/clients/{client_uid}")
async def get_client(client_uid: int):
    # TODO: Lookup query param without trailing /
    if client_uid not in client_repo.data:
        raise HTTPException(status_code=404, 
                detail=f"Client with ID `{client_uid}` not found")
    client = client_repo.data[client_uid]
    return client


@app.get("/products")
async def get_products():
    return prod_repo.data


@app.get("/products/{product_uid}")
async def get_product(product_uid: int):
    if product_uid not in prod_repo.data:
        raise HTTPException(status_code=404, 
                detail=f"Product with ID `{product_uid}` not found")
    return prod_repo.data[product_uid]


class ClientInputModel(BaseModel):
    first_name: str
    last_name: str

@app.post("/clients")
async def create_client(client_data: ClientInputModel):
    client_repo.add(None, Client(None, 
                                 first_name=client_data.first_name,
                                 last_name=client_data.last_name))
    return client_data


class ProductInputModel(BaseModel):
    name: str


@app.post("/products")
async def create_product(product_data: ProductInputModel):
    prod_repo.add(None, Product(None, name=product_data.name))
    return product_data


@app.get("/clients/{client_uid}/products/{product_uid}/balance")
async def get_client_balance(client_uid: int, product_uid: int):
    balances = {}
    for acc_number, value in prod_client_repo.data.items():
        if value.client_uid == client_uid and value.product_uid == product_uid:
            # TODO without specific balances[acc_number] = {"balance": value.params["balance"]}
            balances[acc_number] = {"balance": value.params["balance"],
                                    "currency": value.params["currency"]}
            
    return balances



# POST metoda   (businesově vytvářím transakci)
# přijímá ODKUD, KAM, KOLIK   (ID účtu, ID účtu, float)
# kontroluje dostatečné množství peněz na účtu ODKUD
# provede transakci v datamodelu







