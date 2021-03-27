from app import app
from app.database import db
from app.database.models import DeployedModel, User
from starlette import status
from starlette.responses import Response


@app.get("/model/fetch-one")
async def fetch_one(uid: str, resp: Response):
    model = (
        db.query(DeployedModel, User.username).filter(DeployedModel.uid == uid).one()
    )
    if not model:
        resp.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No model found for given UID"}
    return {"result": "ok", "model": model}
