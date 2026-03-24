import os
from fastapi import FastAPI, Query, Path
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson.objectid import ObjectId

app = FastAPI(title="Reactive Microservice")

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://mongo:27017/reactive_db")

client = AsyncIOMotorClient(MONGODB_URL)
db = client.reactive_db

class Item(BaseModel):
    name: str
    description: str = None
    price: float = None

@app.get("/")
async def root():
    return {"message": "Reactive Microservice with Python"}

@app.get("/search")
async def search(q: str = Query(..., min_length=1), skip: int = 0, limit: int = 10):
    items = await db.items.find({"name": {"$regex": q, "$options": "i"}}).skip(skip).limit(limit).to_list(limit)
    return {"query": q, "results": items, "count": len(items)}

@app.get("/items/{item_id}")
async def get_item(item_id: str = Path(..., description="Item ID")):
    item = await db.items.find_one({"_id": ObjectId(item_id)})
    if item:
        item["_id"] = str(item["_id"])
    return item

@app.post("/items/")
async def create_item(item: Item):
    result = await db.items.insert_one(item.model_dump())
    return {"id": str(result.inserted_id), "created": True}

@app.post("/items/batch")
async def create_items_batch(items: list[Item], notify: bool = Query(False)):
    result = await db.items.insert_many([item.model_dump() for item in items])
    return {"inserted": len(result.inserted_ids), "notify": notify, "ids": [str(id) for id in result.inserted_ids]}

@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    result = await db.items.update_one({"_id": ObjectId(item_id)}, {"$set": item.model_dump(exclude_unset=True)})
    return {"updated": result.modified_count > 0}

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = await db.items.delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count > 0}

@app.get("/items")
async def list_items(skip: int = Query(0), limit: int = Query(10)):
    items = await db.items.find().skip(skip).limit(limit).to_list(limit)
    for item in items:
        item["_id"] = str(item["_id"])
    return {"items": items, "count": len(items)}
