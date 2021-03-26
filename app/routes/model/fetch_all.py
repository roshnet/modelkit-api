from app import app
from app.database import db
from app.database.models import DeployedModel, User
from starlette import status
from starlette.responses import Response


@app.get("/model/fetch-all")
async def fetch_all(username: str, resp: Response):
    # TODO: Add token validation part

    models = db.query(DeployedModel).join(User).filter(User.username == username).all()
    if not models:
        resp.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No models found for given username"}
    return {"result": "ok", "models": models}
