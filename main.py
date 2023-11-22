from fastapi import FastAPI, HTTPException

from datamodel import ClientRepository, ProductRepository

app = FastAPI()

clients_repo = ClientRepository()
product_repo = ProductRepository()

@app.get("/status")
async def root():
    return {"message": "OK"}


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