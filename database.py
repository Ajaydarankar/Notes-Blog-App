from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})

Session_Local = sessionmaker(autocommit = False,autoflush=False,bind = engine)
Base = declarative_base()

def get_db():
    db = Session_Local()
    try:
        yield db
    finally:
        db.close()
