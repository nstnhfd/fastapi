from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker,declarative_base
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base
import pytest
from alembic import command


#SQLALCHEMY_DATABASE_URL = 'postgres://postgres:password123@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

#app.dependency_overrides[get_db] = overrid_get_db
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

#client = TestClient(app)
@pytest.fixture()
def client(session): 
   def overrid_get_db():
    
        try:
            yield session
        finally:
            session.close()    
    
   app.dependency_overrides[get_db] = overrid_get_db
   yield TestClient(app)
    
    

