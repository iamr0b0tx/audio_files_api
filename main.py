from typing import List, Union, Optional, Literal

from fastapi import Depends, FastAPI, HTTPException, Response, Request
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine
from db.exceptions import InvalidAudioType, AudioDoesNotExist
from db.schemas import AudioFileType, AudioTypeSchemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# middleware
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)

    finally:
        request.state.db.close()

    return response


# Dependency
def get_db(request: Request):
    return request.state.db


@app.post("/", response_model=AudioTypeSchemas)
def create_audio(audio: schemas.AudioCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_audio_file(db=db, audio=audio)

    except InvalidAudioType:
        raise HTTPException(status_code=404, detail="Invalid AudioFile type!")


# @app.get("/{audio_file_type}/", response_model=List[AudioTypeSchemas])
@app.get("/{audio_file_type}/{audio_id}", response_model=AudioTypeSchemas)
def read_user(audio_file_type: AudioFileType, audio_id: Optional[int] = None,
              skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    # retrieves a list of audio objects
    if audio_id is None:
        return crud.get_audio_files(db, audio_file_type=audio_file_type, skip=skip, limit=limit)

    # retrieves specific audio file
    try:
        return crud.get_audio_file(db, audio_file_type=audio_file_type, audio_id=audio_id)

    except AudioDoesNotExist:
        raise HTTPException(status_code=404, detail="AudioFile not found!")
