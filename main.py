from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from database import create_itemDb, get_all_items, get_item, update_item, delete_item, delete_database
import secrets

app = FastAPI()
security = HTTPBasic()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"


def admin_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


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
def update_item_by_id(id: int, item: Item, _: bool = Depends(admin_auth)):
    updated_item = update_item(id, item.name, item.description)
    if updated_item:
        return {"item": id, "message": "Item updated successfully"}
    return {"error": "Item not found"}

@app.post("/item/add")
def create_item(item: Item, _: bool = Depends(admin_auth)):
    new_item = create_itemDb(item.name, item.description)
    return {"item": new_item.id, "message": "Item created successfully"}

@app.delete("/item/delete/{id}")
def delete_item_by_id(id: int, _: bool = Depends(admin_auth)):
    if delete_item(id):
        return {"item": id, "message": "Item deleted successfully"}
    return {"error": "Item not found"}

@app.get("/deleteDB")
def clear_database(_: bool = Depends(admin_auth)):
    delete_database()
    return {"message": "Database reset successfully"}