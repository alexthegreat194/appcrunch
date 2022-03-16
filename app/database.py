from sqlmodel import SQLModel, create_engine
from .models import User, Idea, Upvote, Comment

db_url = 'sqlite:///database.db'
engine = create_engine(db_url)

def create_db_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == '__main__':
    print('creating db...')
    create_db_tables()