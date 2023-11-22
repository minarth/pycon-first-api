from fastapi import FastAPI

from datamodel import ClientRepository

app = FastAPI()

clients_repo = ClientRepository()

@app.get("/status")
async def root():
    return {"message": "OK"}


@app.get("/clients")
async def get_clients():
    return clients_repo.data

