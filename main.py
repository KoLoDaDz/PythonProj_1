from fastapi import FastAPI
from pydantic import BaseModel, Field
from database import create_itemDb, get_all_items, get_item, update_item, delete_item, delete_database

app = FastAPI()

class Item(BaseModel):
    name: str = Field(max_length=20)
    description: str = Field(default=None, max_length=200)



@app.get("/")
def get_all_item():
    return get_all_items()

@app.get("/item/{id}")
def get_item_by_id(id: int):
    return get_item(id)


@app.put("/item/update/{id}")
def update_item_by_id(id: int, item: Item):
    updated_item = update_item(id, item.name, item.description)
    if updated_item:
        return {"item": id, "message": "Item updated successfully"}
    return {"error": "Item not found"}


@app.post("/item/add")
def create_item(item: Item):
    new_item = create_itemDb(item.name, item.description)
    return {"item": new_item.id, "message": "Item created successfully"}

@app.delete("/item/delete/{id}")
def delete_item_by_id(id: int):
    if delete_item(id):
        return {"item": id, "message": "Item deleted successfully"}
    return {"error": "Item not found"}
    

@app.get("/deleteDB")
def clear_database():
    delete_database()
    return {"message": "Database reset successfully"}
