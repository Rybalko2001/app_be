from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List
from models import BagCreate, BagResponse
#from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url="/api/docs", redoc_url=None, openapi_url="/api/openapi.json")


#app.add_middleware(
 #   CORSMiddleware,
   # allow_origins=["http://localhost:3000"],  # URL React додатку
    #allow_credentials=True,
   # allow_methods=["GET", "POST", "PUT", "DELETE"],
  #  allow_headers=["*"],
#)


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Дозволяє всі походження, змініть на потрібний домен для більшої безпеки
    allow_credentials=True,
    allow_methods=["*"],  # Дозволяє всі методи запитів
    allow_headers=["*"],  # Дозволяє всі заголовки
)


MONGO_DETAILS = "mongodb+srv://nazarrybalko2001:VXIUoTPHKYpCc7Sf@cluster1.3fsedvf.mongodb.net/"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.bag_db
bag_collection = database.get_collection("bags")

@app.post("/api/", response_model=BagResponse)
async def create_bag(bag: BagCreate):
    bag_dict = bag.dict()
    result = await bag_collection.insert_one(bag_dict)
    new_bag = await bag_collection.find_one({"_id": result.inserted_id})
    return BagResponse(id=str(new_bag["_id"]), name=new_bag["name"], brand=new_bag["brand"], price=new_bag["price"])

@app.get("/api/{bag_id}", response_model=BagResponse)
async def read_bag(bag_id: str):
    if not ObjectId.is_valid(bag_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    bag = await bag_collection.find_one({"_id": ObjectId(bag_id)})
    if bag is None:
        raise HTTPException(status_code=404, detail="Bag not found")
    return BagResponse(id=str(bag["_id"]), name=bag["name"], brand=bag["brand"], price=bag["price"])

@app.get("/api/", response_model=List[BagResponse])
async def read_bags(skip: int = 0, limit: int = 10):
    bags_cursor = bag_collection.find().skip(skip).limit(limit)
    bags = await bags_cursor.to_list(length=limit)
    return [BagResponse(id=str(bag["_id"]), name=bag["name"], brand=bag["brand"], price=bag["price"]) for bag in bags]

@app.put("/api/{bag_id}", response_model=BagResponse)
async def update_bag(bag_id: str, updated_bag: BagCreate):
    if not ObjectId.is_valid(bag_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = await bag_collection.update_one({"_id": ObjectId(bag_id)}, {"$set": updated_bag.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Bag not found")
    updated_bag = await bag_collection.find_one({"_id": ObjectId(bag_id)})
    return BagResponse(id=str(updated_bag["_id"]), name=updated_bag["name"], brand=updated_bag["brand"], price=updated_bag["price"])

@app.delete("/api/{bag_id}")
async def delete_bag(bag_id: str):
    if not ObjectId.is_valid(bag_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = await bag_collection.delete_one({"_id": ObjectId(bag_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Bag not found")
    return {"detail": "Bag deleted"}

@app.get("/api/docs", include_in_schema=False)
async def get_custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="API Docs")

@app.get("/api/docs/oauth2-redirect", include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/", status_code=404)
def read_root():
    raise HTTPException(status_code=404, detail="Not found")
