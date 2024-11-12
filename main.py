from typing import Optional

from fastapi import FastAPI

app = FastAPI()

class RequestBody(BaseModel):
    data: Any


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    print('sa')
    return {"item_id": item_id, "q": q}


@app.post("/api2")
def post_item(request_body: RequestBody):
    print(request_body)
    return request_body