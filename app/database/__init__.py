from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://root:aaaaa@localhost/mlrun")

Session = sessionmaker(bind=engine)

db = Session()
