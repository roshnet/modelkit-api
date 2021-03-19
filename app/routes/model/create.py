import os

import jwt
from app import app
from app.database import db
from fastapi import File, Request, UploadFile

STORAGE_DIR = os.path.join(os.getcwd(), "storage")


@app.post("/model/create")
async def create_model(req: Request, model: UploadFile = File(...)):
    if "x-model-author" not in req.headers.keys():
        return {"result": "fail", "reason": "No author specified"}

    if not os.path.exists(STORAGE_DIR):
        os.mkdir(STORAGE_DIR)

    filename = model.filename
    with open(os.path.join(STORAGE_DIR, filename), "wb") as fp:
        fp.write(model.file.read())

    # TODO: Validate token

    return {"filename": filename}
