from app import app
from app.database import db
from app.database.models import DeployedModel as Model
from app.database.models import User


@app.get("/feed")
async def feed(start=0, count=10):
    models = db.query(Model).join(User).offset(start).limit(count).all()
    return {"status": "ok", "models": models}
