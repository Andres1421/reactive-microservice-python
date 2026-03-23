from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson.objectid import ObjectId

app = FastAPI(title="Reactive Microservice")

# Conexión async a MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.reactive_db

class Item(BaseModel):
    name: str
    description: str = None

@app.get("/")
async def root():
    return {"message": "Reactive Microservice with Python"}

@app.post("/items/")
async def create_item(item: Item):
    result = await db.items.insert_one(item.model_dump())
    return {"id": str(result.inserted_id)}

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    item = await db.items.find_one({"_id": ObjectId(item_id)})
    if item:
        item["_id"] = str(item["_id"])
    return item
