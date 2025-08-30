import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from backend.app import app
from backend.db.database import Base, get_db

# Create a temporary SQLite database for testing
@pytest.fixture(scope="function")
def test_db():
    # Use a temporary file-based SQLite database
    db_fd, db_path = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Provide a new session for each test
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestingSessionLocal

    # Cleanup after test
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    os.close(db_fd)
    os.unlink(db_path)
    clear_mappers()


# Fixture to get the FastAPI test client
@pytest.fixture(scope="function")
def client(test_db):
    with TestClient(app) as c:
        yield c
