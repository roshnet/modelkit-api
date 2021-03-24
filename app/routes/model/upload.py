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

STORAGE_DIR = os.path.join(os.getcwd(), "storage")


@app.post("/model/upload")
async def create_model(req: Request, resp: Response, model: UploadFile = File(...)):
    if "X-Auth-Token".lower() not in req.headers.keys():
        resp.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": "fail", "reason": "No auth token specified"}

    token = req.headers["X-Auth-Token"]
    try:
        _ = json.loads(
            json.dumps(jwt.decode(token, ACCESS_TOKEN_KEY, algorithms="HS256"))
        )
    except Exception as e:
        resp.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": "fail", "reason": str(e)}

    if "X-Model-Id".lower() not in req.headers.keys():
        resp.status_code = status.HTTP_400_BAD_REQUEST
        return {"result": "fail", "reason": "No model entry specified"}

    # TODO: Check header key case
    model_uid = req.headers["X-Model-Id"]

    if not os.path.exists(STORAGE_DIR):
        os.mkdir(STORAGE_DIR)

    try:
        with open(os.path.join(STORAGE_DIR, model_uid), "wb") as fp:
            fp.write(model.file.read())
    except Exception as e:
        resp.status_code = status.HTTP_507_INSUFFICIENT_STORAGE
        return {"result": "fail", "reason": str(e)}

    return {"result": "ok"}
