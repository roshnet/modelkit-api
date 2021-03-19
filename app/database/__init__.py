from app.config import SQLALCHEMY_CONNECTION_STRING
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(SQLALCHEMY_CONNECTION_STRING)

Session = sessionmaker(bind=engine)

db = Session()
