import pytest
from decouple import config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from db.crud import create_audio_file
from db.database import Base
from db.schemas import SongCreateSchema, AudiobookCreateSchema, PodcastCreateSchema
from main import app, get_db

SQLALCHEMY_DATABASE_URL = config("TEST_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db() -> Session:
    db_session = TestingSessionLocal()
    try:
        yield db_session

    finally:
        db_session.close()


db = next(iter(override_get_db()))
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

audio1 = create_audio_file(db, "song", SongCreateSchema(
    name="The sound of music",
    duration=120
))

audio2 = create_audio_file(db, "podcast", PodcastCreateSchema(
    name="Python Bytes",
    duration=300,
    host="Michael Kennedy",
    participants=["Michael Kennedy", "Brian Okken", "Guido Van Rossum"]

))

audio3 = create_audio_file(db, "audiobook", AudiobookCreateSchema(
    title="Orphan Black",
    duration=900,
    author="George R.R Martin",
    narrator="Samwell Tarly"
))

print(audio1.id)
print(audio2.id)
print(audio3.id)


# generic test
def test_get_audio():
    response = client.get('/')
    assert response.status_code == 405


@pytest.mark.parametrize(
    "data, status_code",
    [
        # valid song creation
        ({
             "audioFileType": "song",
             "audioFileMetaData": {
                 "name": "The sound of music",
                 "duration": 190
             }
         }, 200),
        # song creating with invalid audio file type
        ({
             "audioFileType": "invalid",
             "audioFileMetaData": {
                 "name": "The sound of music",
                 "duration": 190
             }
         }, 422),
        ({
             "audioFileType": "podcast",
             "audioFileMetaData": {
                 "name": "Planet Earth",
                 "duration": 1200,
                 "host": "Jerry",
                 "participants": ["jane", "kelly"]
             }
         }, 200),
        ({
             "audioFileType": "podcast",
             "audioFileMetaData": {
                 "name": "Planet Earth",
                 "duration": 1200,
                 "host": "Jerry",
                 "participants": [
                     "jane", "kelly", "harry", "june", "peter", "larry", "scott", "berry", "paige", "kenny", "wanda"
                 ]
             }
         }, 422),
        ({
             "audioFileType": "audiobook",
             "audioFileMetaData": {
                 "title": "The Art of war",
                 "duration": 4000,
                 "author": "Sun Tzu",
                 "narrator": "Morgan Freeman"
             }
         }, 200),
    ]
)
def test_post_audio(data, status_code):
    response = client.post('/', json=data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "audio_file_type, status_code",
    [
        ("", 405),
        ("invalid", 422),
        ("song", 200),
        ("podcast", 200),
        ("audiobook", 200),
    ]
)
def test_read_all_audio(audio_file_type, status_code):
    response = client.get(f'/{audio_file_type}')
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "audio_file_type, audio_id, status_code",
    [
        ("", "", 405),
        ("", 0, 405),
        ("invalid", "", 422),
        ("", "invalid", 405),
        ("song", 1, 200),
        ("song", 0, 404),
    ]
)
def test_read_audio_object(audio_file_type, audio_id, status_code):
    response = client.get(f'/{audio_file_type}/{audio_id}')
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "data, audio_id, status_code",
    [
        # valid song creation
        ({
             "audioFileType": "song",
             "audioFileMetaData": {
                 "name": "The sound of music 2",
                 "duration": 200
             }
         }, 1, 200),
        # song creating with invalid audio file type
        ({
             "audioFileType": "invalid",
             "audioFileMetaData": {
                 "name": "The sound of music 2",
                 "duration": 200
             }
         }, 1, 422),
        ({
             "audioFileType": "podcast",
             "audioFileMetaData": {
                 "name": "Planet Earth",
                 "duration": 1200,
                 "host": "Jerry",
                 "participants": ["jane", "kelly"]
             }
         }, 1, 200),
        ({
             "audioFileType": "podcast",
             "audioFileMetaData": {
                 "name": "Planet Earth",
                 "duration": 1200,
                 "host": "Jerry",
                 "participants": [
                     "jane", "kelly", "harry", "june", "peter", "larry", "scott", "berry", "paige", "kenny", "wanda"
                 ]
             }
         }, 1, 422),
        ({
             "audioFileType": "audiobook",
             "audioFileMetaData": {
                 "title": "The Art of war",
                 "duration": 4000,
                 "author": "Sun Tzu",
                 "narrator": "Morgan Freeman"
             }
         }, 1, 200),
        ({
             "audioFileType": "audiobook",
             "audioFileMetaData": {
                 "title": "The Art of war",
                 "duration": 4000,
                 "author": "Sun Tzu",
                 "narrator": "Morgan Freeman"
             }
         }, 99, 404),
    ]
)
def test_update_audio(data, audio_id, status_code):
    audio_file_type = data.get("audioFileType", "")
    response = client.put(f'/{audio_file_type}/{audio_id}', json=data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "audio_file_type, audio_id, status_code",
    [
        # a valid type existing in db
        ("song", 1, 200),

        # using an invalid audio type
        ("invalid", 1, 422),

        # delete already existing
        ("podcast", 1, 200),

        # test post deletion
        ("podcast", 1, 404),
        ("audiobook", 1, 200),
        ("audiobook", 99, 404),
    ]
)
def test_delete_audio(audio_file_type, audio_id, status_code):
    response = client.delete(f'/{audio_file_type}/{audio_id}')
    assert response.status_code == status_code
