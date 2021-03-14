from fastapi import FastAPI

app = FastAPI()

USERNAME = "rosh"
PASSWORD = "rosh"

from app import routes  # noqa


@app.get("/")
async def home():
    return {"status": "OK"}
