from datetime import datetime, timedelta

import jwt
from app import app
from app.database import db
from app.database.models import User
from fastapi import Request
from fastapi.responses import JSONResponse

SECRET_KEY = "loadthisfromenv"


@app.post("/login")
async def login(request: Request):
    body = await request.json()
    payload = {
        "exp": datetime.utcnow() + timedelta(days=0, hours=24),
        "iat": datetime.utcnow(),
    }
    u, p = body["username"], body["password"]

    result = db.query(User).filter_by(username=u, password_hash=p).first()
    if result is not None:
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256").decode("utf-8")
        content = {"result": "ok"}
        response = JSONResponse(content=content)
        response.headers["X-AUTH-TOKEN"] = f"{(token)}"
        return response
    return {"result": "fail"}
