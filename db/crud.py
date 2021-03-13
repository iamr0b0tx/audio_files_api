from sqlalchemy.orm import Session

from . import models, schemas
from .exceptions import AudioDoesNotExist, UpdateError, DeleteError
from .schemas import AudioFileType, AudioCreateTypeSchemas

type_model_map = {
    'song': models.Song,
    'podcast': models.Podcast,
    'audiobook': models.Audiobook
}


def get_audio_model(audio_file_type: AudioFileType):
    return type_model_map[audio_file_type]


def get_audio_file(db: Session, audio_file_type: AudioFileType, audio_id: int):
    audio_model = get_audio_model(audio_file_type)
    audio_object = db.query(audio_model).get(audio_id)

    if audio_object is None:
        raise AudioDoesNotExist()

    return audio_object


def get_audio_files(db: Session, audio_file_type: AudioFileType, skip: int = 0, limit: int = 100):
    audio_model = get_audio_model(audio_file_type)
    return db.query(audio_model).offset(skip).limit(limit).all()


def create_audio_file(db: Session, audio_file_type: AudioFileType, audio_file_metadata: AudioCreateTypeSchemas):
    audio_model = get_audio_model(audio_file_type)
    audio_object = audio_model(**audio_file_metadata.dict())

    db.add(audio_object)
    db.commit()
    db.refresh(audio_object)
    return audio_object


def update_audio_file(db: Session, audio_file_type: AudioFileType,
                      audio_id: int, audio_file_metadata: AudioCreateTypeSchemas):

    audio_model = get_audio_model(audio_file_type)
    audio_object_id = db.query(audio_model).filter_by(id=audio_id).update(audio_file_metadata.dict())

    if not audio_object_id:
        raise AudioDoesNotExist()

    if audio_object_id != audio_id:
        raise UpdateError()

    db.commit()
    return audio_object_id


def delete_audio_file(db: Session, audio_file_type: AudioFileType,audio_id: int):

    audio_model = get_audio_model(audio_file_type)
    audio_object_id = db.query(audio_model).filter_by(id=audio_id).delete()

    if not audio_object_id:
        raise AudioDoesNotExist()

    if audio_object_id != audio_id:
        raise DeleteError()

    db.commit()
    return audio_object_id
