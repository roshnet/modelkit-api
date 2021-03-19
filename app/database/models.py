from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    name = Column(String(30))
    models = relationship("DeployedModel", backref="author")
    password_hash = Column(String(512))


class DeployedModel(Base):
    __tablename__ = "models"
    model_id = Column(Integer, primary_key=True)
    name = Column(String(30))
    author_id = Column(Integer, ForeignKey(User.id))
    description = Column(String(1000))
