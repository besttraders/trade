from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Any
import sqlite3
import uuid
import random

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

class Student(BaseModel):
    isim: str
    yas: int

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    print('sa')
    return {"item_id": item_id, "q": q}

@app.get("/students")
def read_items(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT isim, yas FROM ogrenciler")
    data = cursor.fetchall()
    return [{"isim": isim, "yas": yas} for isim, yas in data]

@app.post("/create_student", response_model=Student)
def create_random_student(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    
    random_name = random.choice(["Ahmet", "Elif", "Mehmet", "Zeynep", "Veli", "Fatma", "Ali", "Ayşe"])
    random_age = random.randint(18, 30)  # Age between 18 and 30

    try:
        cursor.execute("INSERT INTO ogrenciler (isim, yas) VALUES (?, ?)", (random_name, random_age))
        db.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    return Student(isim=random_name, yas=random_age)


class Item(BaseModel):
    data: str

@app.post("/echo")
def echo_item(item: Item):
    return item