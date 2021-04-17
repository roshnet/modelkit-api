import os
from typing import List

import joblib
from app import app
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response

STORAGE_DIR = os.path.join(os.getcwd(), "storage")


class RequestBody(BaseModel):
    model_uid: str
    xtest: List


@app.post("/predict")
async def train(req: RequestBody, resp: Response):
    model_file = os.path.join(STORAGE_DIR, req.model_uid)

    try:
        clf = joblib.load(open(model_file, "rb"))
    except FileNotFoundError:
        resp.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "fail", "reason": "Model binary not found"}
    if not hasattr(clf, "predict"):
        return {"status": "ok"}

    try:
        prediction = clf.predict(req.xtest)
    except Exception as e:
        resp.status_code = status.HTTP_417_EXPECTATION_FAILED
        return {"status": "fail", "reason": str(e)}

    return {"status": "ok", "prediction": str(prediction)}
