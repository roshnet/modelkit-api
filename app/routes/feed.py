from typing import Optional

from app import app
from app.database import db, models
from app.database.models import DeployedModel as Model
from app.database.models import User
from pydantic import BaseModel


class RequestBody(BaseModel):
    start: Optional[int] = 0
    count: Optional[int] = 10


@app.get("/feed")
async def feed(req: RequestBody):
    models = db.query(Model).join(User).offset(req.start).limit(req.count).all()

    return {"status": "ok", "models": models}
