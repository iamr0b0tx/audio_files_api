import pytest
from decouple import config

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = config("TEST_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_audio():
    response = client.get('/')
    assert response.status_code == 405


@pytest.mark.parametrize(
    "audio_file_type, audio_id, status_code",
    [
        ("", "", 405),
        ("", 0, 405),
        ("invalid", "", 404),
        ("", "invalid", 405),
        ("song", 0, 200),
        ("song", 99, 404),
    ]
)
def test_get_audio_object(audio_file_type, audio_id, status_code):
    response = client.get(f'/{audio_file_type}/{audio_id}')
    print(response.content)
    assert response.status_code == status_code


def test_post_audio():
    response = client.post('/audio/', data={})
    assert response.status_code == 404
