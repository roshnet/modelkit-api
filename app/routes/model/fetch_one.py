from app import app
from app.database import db
from app.database.models import DeployedModel, User
from starlette import status
from starlette.responses import Response


@app.get("/model/fetch-one")
async def fetch_one(uid: str, resp: Response):
    # TODO: Choose between .first() and .one() to fetch a model.
    # Using .one() throws an exception for zero or >1 results, hence using .first().
    model = (
        db.query(DeployedModel.name, DeployedModel.description, User.username)
        .join(User)
        .filter(DeployedModel.uid == uid)
        .first()
    )
    if not model:
        resp.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No model found for given UID"}

    return {"result": "ok", "model": model}
