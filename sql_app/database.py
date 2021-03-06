from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import config

SQLALCHEMY_DATABASE_URL = 'sqlite:///test.db'
if config.MYSQL_CONNECTION_URL is not None:
    print("Using MySQL")
    SQLALCHEMY_DATABASE_URL = config.MYSQL_CONNECTION_URL
elif config.POSTGRES_CONNECTION_URL is not None:
    print("Using postgres")
    SQLALCHEMY_DATABASE_URL = config.POSTGRES_CONNECTION_URL
else:
    print("Using SQLLITE")

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
