from sqlmodel import SQLModel, create_engine
from .models import *

db_url = 'sqlite://database.db'
engine = create_engine(db_url, echo=True)

def create_db_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == '__main__':
    create_db_tables()