import hashlib
from datetime import datetime, timedelta

import jwt
from app import app
from app.config import ACCESS_TOKEN_KEY
from app.database import db
from app.database.models import User
from fastapi import Request
from fastapi.responses import JSONResponse


@app.post("/login")
async def login(request: Request):
    body = await request.json()
    u = body["username"]
    p = hashlib.sha256(str.encode(body["password"])).hexdigest()

    result = db.query(User).filter_by(username=u, password_hash=p).first()
    if result is None:
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
