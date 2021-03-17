from datetime import datetime, timedelta

import jwt
from app import app
from fastapi import Request
from fastapi.responses import JSONResponse

USERNAME = "rosh"
PASSWORD = "rosh"
SECRET_KEY = "loadthisfromenv"


@app.post("/login")
async def login(request: Request):
    body = await request.json()
    payload = {
        "exp": datetime.utcnow() + timedelta(days=0, hours=24),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256").decode("utf-8")
    u = body["username"]
    p = body["password"]
    if u == USERNAME and p == PASSWORD:
        content = {"result": "ok"}
        response = JSONResponse(content=content)
        response.headers["X-AUTH-TOKEN"] = f"{(token)}"
        return response
    return {"result": "fail"}
