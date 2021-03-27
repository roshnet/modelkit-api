import hashlib
from datetime import datetime, timedelta

import jwt
from app import app
from app.config import ACCESS_TOKEN_KEY
from app.database import db
from app.database.models import User
from fastapi import Response, status
from pydantic import BaseModel
from starlette.responses import JSONResponse


class RequestBody(BaseModel):
    username: str
    name: str
    password: str


@app.post("/signup")
async def signup(body: RequestBody, response: Response):
    username = body.username
    name = body.name
    password_hash = hashlib.sha256(str.encode(body.password)).hexdigest()

    # Check if username already exists
    exists = db.query(User).filter_by(username=username).first()
    if exists:
        response.status_code = status.HTTP_409_CONFLICT
        return {"result": "fail", "reason": "Username already taken"}

    user = User(username=username, name=name, password_hash=password_hash)
    db.add(user)
    db.commit()

    payload = {
        "exp": datetime.utcnow() + timedelta(days=0, hours=24),
        "iat": datetime.utcnow(),
        "iss": username,
    }
    token = jwt.encode(payload, ACCESS_TOKEN_KEY, algorithm="HS256")
    content = {"result": "ok"}
    response = JSONResponse(content=content)
    response.headers["X-AUTH-TOKEN"] = f"{token}"
    return response
