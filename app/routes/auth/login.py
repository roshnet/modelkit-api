import hashlib
from datetime import datetime, timedelta

import jwt
from app import app
from app.config import ACCESS_TOKEN_KEY
from app.database import db
from app.database.models import User
from fastapi import Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class RequestBody(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(body: RequestBody, response: Response):
    u = body.username
    p = hashlib.sha256(str.encode(body.password)).hexdigest()

    result = db.query(User).filter_by(username=u, password_hash=p).first()
    if result is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": "fail", "reason": "Incorrect credentials"}

    payload = {
        "exp": datetime.utcnow() + timedelta(days=0, hours=24),
        "iat": datetime.utcnow(),
        "iss": u,
    }
    token = jwt.encode(payload, ACCESS_TOKEN_KEY, algorithm="HS256")
    content = {"result": "ok"}
    response = JSONResponse(content=content)
    response.headers["X-AUTH-TOKEN"] = f"{token}"
    return response
