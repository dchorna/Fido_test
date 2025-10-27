from fastapi import FastAPI
from fastapi import HTTPException
import uvicorn
from pydantic import BaseModel
import weaviate
import os
from weaviate.classes.init import Auth
from weaviate.classes.config import Property, DataType, Configure

app = FastAPI()

items = []

WEAVIATE_URL = "https://coumhlshszx2klnfssrq.c0.europe-west3.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "bUFBZ2xIR25wTi9FaDRQYl83Z2lyeHFGYUNFT2gyUzZvUllyK0pvTDNIOGEvakYzQndBRlBxRk5xcno0PV92MjAw"

client = weaviate.connect_to_weaviate_cloud(
    cluster_url= "https://coumhlshszx2klnfssrq.c0.europe-west3.gcp.weaviate.cloud",
    auth_credentials=Auth.api_key("bUFBZ2xIR25wTi9FaDRQYl83Z2lyeHFGYUNFT2gyUzZvUllyK0pvTDNIOGEvakYzQndBRlBxRk5xcno0PV92MjAw"),
)

print(client.is_ready())

def weaviate_sh():
    properties = [
        Property(name = "name", data_type = DataType.TEXT),#передаємо аргумент 
        Property(name = "preice", data_type=DataType.NUMBER)
    ]

vectorizer_config = Configure.Vectorizer.text2vec_azure_openai(model="ada")

class Item(BaseModel): #клас для перевірки типів двних
    text: str = None #text: є поле текст
    is_done: bool = False # якщо ніяке значення не передано 

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/items", response_model=list[Item])
def lim_items(limit: int = 10):
    return items[0:limit]


@app.post("/items", status_code=201) # записувати дані, 201 - стандартний код, запит оброблено
def create_item(item: Item): # приймає на ввід параметр
    items.append(item) #додає в список
    return items #повертає, тобто друкує

@app.get("/items/{item_id}", response_model=Item)# повертає тільки елемент з потрібним id 
def get_item(item_id: int) -> Item: # функція яка перетворить параметр у число
    if item_id < len(items):
        return items[item_id]
    else: raise HTTPException(status_code=404, detail="Item not found")