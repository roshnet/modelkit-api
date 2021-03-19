from app.database import engine
from app.database.models import DeployedModel, User

User.__table__.create(engine)
DeployedModel.__table__.create(engine)
