from app import app
from fastapi import Request

USERNAME = "rosh"
PASSWORD = "rosh"


@app.post("/login")
async def login(request: Request):
    body = await request.json()
    u = body["username"]
    p = body["password"]
    if u == USERNAME and p == PASSWORD:
        return {"token": "58g84yckr8tbuwsk04j"}
    return {}
