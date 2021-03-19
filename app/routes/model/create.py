import json
import os

import jwt
from app import app
from app.config import ACCESS_TOKEN_KEY
from app.database import db
from app.database.models import DeployedModel, User
from fastapi import File, Request, UploadFile, status
from starlette.responses import Response

STORAGE_DIR = os.path.join(os.getcwd(), "storage")


@app.post("/model/create")
async def create_model(req: Request, resp: Response, model: UploadFile = File(...)):
    if "X-Auth-Token".lower() not in req.headers.keys():
        resp.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": "fail", "reason": "No auth token specified"}

    token = req.headers["X-Auth-Token"]
    try:
        decoded = json.loads(
            json.dumps(jwt.decode(token, ACCESS_TOKEN_KEY, algorithms="HS256"))
        )
    except Exception as e:
        resp.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": "fail", "reason": str(e)}

    if "X-Model-Author".lower() not in req.headers.keys():
        resp.status_code = status.HTTP_400_BAD_REQUEST
        return {"result": "fail", "reason": "No author specified"}

    # TODO: Check header key case
    username = req.headers["X-Model-Author"]

    if not os.path.exists(STORAGE_DIR):
        os.mkdir(STORAGE_DIR)

    filename = f"{username}-{model.filename}"
    try:
        with open(os.path.join(STORAGE_DIR, filename), "wb") as fp:
            fp.write(model.file.read())
    except Exception as e:
        resp.status_code = status.HTTP_507_INSUFFICIENT_STORAGE
        return {"result": "fail", "reason": str(e)}

    try:
        user = db.query(User).filter_by(username=username).first()
        m = DeployedModel(name=filename, author=user, description="OK")
        db.add(m)
        db.commit()
    except Exception as e:
        return {"result": "fail", "reason": str(e)}

    return {"result": "ok", "filename": filename}
