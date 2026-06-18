from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///data.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    age = Column(Integer)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()