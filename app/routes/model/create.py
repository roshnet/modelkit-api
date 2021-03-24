import json
import os
import uuid

import jwt
from app import app
from app.config import ACCESS_TOKEN_KEY
from app.database import db
from app.database.models import DeployedModel, User
from fastapi import File, Request, UploadFile, status
from starlette.responses import Response


@app.post("/model/create")
async def create_model(req: Request, resp: Response):
    if "X-Auth-Token".lower() not in req.headers.keys():
        resp.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": "fail", "reason": "No auth token specified"}

    # TODO: Check header key case
    token = req.headers["X-Auth-Token"]
    try:
        _ = json.loads(
            json.dumps(jwt.decode(token, ACCESS_TOKEN_KEY, algorithms="HS256"))
        )
    except Exception as e:
        resp.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": "fail", "reason": str(e)}

    # TODO: Use pydantic models to auto-validate body params
    body = await req.json()
    name = body["name"]
    username = body["username"]
    description = body["description"]

    uid_slug = uuid.uuid4().hex[:6]
    model_uid = f"{username}-{uid_slug}"
    try:
        user = db.query(User).filter_by(username=username).first()
        m = DeployedModel(
            name=name, uid=model_uid, author=user, description=description
        )
        db.add(m)
        db.commit()
    except Exception as e:
        db.rollback()
        resp.status_code = status.HTTP_400_BAD_REQUEST
        return {"result": "fail", "reason": str(e)}

    return {"result": "ok", "uid": model_uid}
