from typing import Optional

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Any
import sqlite3

app = FastAPI()

with sqlite3.connect('mydb.db') as db:
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS ogrenciler")
    cursor.execute("CREATE TABLE ogrenciler(isim TEXT, yas INTEGER)")
    db.commit()
    
def get_db():
    db = sqlite3.connect('mydb.db')
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    print('sa')
    return {"item_id": item_id, "q": q}

@app.get("/items")
def read_items(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT isim, yas FROM ogrenciler")
    data = cursor.fetchall()
    return [{"isim": isim, "yas": yas} for isim, yas in data]

@app.post("/api2")
def post_item(request_body):
    print(request_body)
    return request_body