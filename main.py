from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    print('sa')
    return {"item_id": item_id, "q": q}


@app.post("/api2")
def post_item(request_body):
    print(request_body)
    return request_body