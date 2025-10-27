from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
import uvicorn
import weaviate
import os
from weaviate.classes.init import Auth
from weaviate.classes.config import Property, DataType, Configure

app = FastAPI()

my_notes = []

WEAVIATE_URL = "https://zakkydo9svybecspbi7p3w.c0.europe-west3.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "bUFBZ2xIR25wTi9FaDRQYl83Z2lyeHFGYUNFT2gyUzZvUllyK0pvTDNIOGEvakYzQndBRlBxRk5xcno0PV92MjAw"

client = weaviate.connect_to_weaviate_cloud(
    cluster_url= "https://zakkydo9svybecspbi7p3w.c0.europe-west3.gcp.weaviate.cloud",
    auth_credentials=Auth.api_key("bUFBZ2xIR25wTi9FaDRQYl83Z2lyeHFGYUNFT2gyUzZvUllyK0pvTDNIOGEvakYzQndBRlBxRk5xcno0PV92MjAw"),
)

print(client.is_ready())

def Notes():
    schem = {
        "class": "Notes",
        "vectorizer": "text2vec-openai",
        "properties": [
           {"name": "text", "dataType": ["text"]},
           {"name": "importance", "dataType": ["int"]},
           {"name": "is_done", "dataType": ["boolean"]}
        ]
    }

if not client.collections.exists("Notes"):
    client.collections.create(
        name="Notes",
        properties=[
            Property(name = "text", data_type=DataType.TEXT),
            Property(name = "importance", data_type=DataType.INT),
            Property(name = "is_done", data_type=DataType.BOOL)
        ]
    )

vectorizer_config = Configure.Vectorizer.text2vec_azure_openai(model="ada")

class Note(BaseModel):
    text: str = None
    is_done: bool = False
    importance: int = None


@app.post("/Notes", status_code=201)
def create_note(item: Note):
    obj = {"text": item.text, "importance": item.importance, "is_done": item.is_done}
    result = client.data_object.create(obj, "Notes")

@app.get("/Notes/{note_id}", response_model=Note)
def get_note_id(note_id: str):
        note = client.data_object.get(note_id, "Notes")
        return note

@app.get("/search")
def search_note(q: str, limit: int = 15):
     result = (
          client.query
          .get("Notes", ["text", "importance", "is_done"])#запит на отриманні об'єктів
          .with_near_text({"concepts": [q]})#пошук за змістом concepts- список слів\фраз\... які ми шукаємо, q передає один рядок
          .with_limit(limit)
          .do()#фактичний запит до weaviate

     )
     res = result.get("data", {}).get("Get", {}).get("Notes", [])# спочатку берем ключ дата, потім словник класів, а потім список всіх нотаток
     return res

     #я старалась))