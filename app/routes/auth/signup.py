import hashlib
from datetime import datetime, timedelta

import jwt
from app import app
from app.config import ACCESS_TOKEN_KEY
from app.database import db
from app.database.models import User
from fastapi import Request
from starlette.responses import JSONResponse


@app.post("/signup")
async def signup(req: Request):
    body = await req.json()
    username = body["username"]
    name = body["name"]
    password_hash = hashlib.sha256(str.encode(body["password"])).hexdigest()

    # Check if username already exists
    exists = db.query(User).filter_by(username=username).first()
    if exists:
        return {"result": "fail", "reason": "Username already taken"}

    user = User(username=username, name=name, password_hash=password_hash)
    db.add(user)
    db.commit()

    payload = {
        "exp": datetime.utcnow() + timedelta(days=0, hours=24),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, ACCESS_TOKEN_KEY, algorithm="HS256")
    content = {"result": "ok"}
    response = JSONResponse(content=content)
    response.headers["X-AUTH-TOKEN"] = f"{token}"
    return response
