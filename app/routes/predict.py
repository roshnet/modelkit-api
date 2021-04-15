import os
from typing import List

import joblib
from app import app
from pydantic import BaseModel

STORAGE_DIR = os.path.join(os.getcwd(), "storage")


class RequestBody(BaseModel):
    model_uid: str
    xtest: List


@app.post("/predict")
async def train(req: RequestBody):
    model_file = os.path.join(STORAGE_DIR, req.model_uid)

    clf = joblib.load(open(model_file, "rb"))

    if not hasattr(clf, "predict"):
        return {"status": "ok"}

    try:
        prediction = clf.predict(req.xtest)
    except Exception as e:
        return {"status": "fail", "reason": str(e)}

    print(prediction)
    return {"status": "ok", "prediction": str(prediction)}
