from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException, Response, Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from db import crud, models, schemas
from db.database import SessionLocal, engine
from db.exceptions import AudioDoesNotExist, UpdateError, DeleteError
from db.schemas import AudioFileType, AudioTypeSchemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# middleware
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = None

    try:
        request.state.db = SessionLocal()
        response = await call_next(request)

    finally:
        request.state.db.close()

        if not response:
            response = Response("Internal server error", status_code=500)

    return response


# Dependency
def get_db(request: Request):
    return request.state.db


@app.post("/", response_model=AudioTypeSchemas)
def create_audio_file(audio: schemas.AudioCreate, db: Session = Depends(get_db)):
    return crud.create_audio_file(
        db=db, audio_file_type=audio.audioFileType, audio_file_metadata=audio.audioFileMetaData
    )


@app.get("/{audio_file_type}", response_model=List[AudioTypeSchemas])
@app.get("/{audio_file_type}/{audio_id}", response_model=AudioTypeSchemas)
def read_audio_file(audio_file_type: AudioFileType, audio_id: Optional[int] = None,
              skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    # retrieves a list of audio objects
    if audio_id is None:
        return crud.get_audio_files(db, audio_file_type=audio_file_type, skip=skip, limit=limit)

    # retrieves specific audio file
    try:
        return crud.get_audio_file(db, audio_file_type=audio_file_type, audio_id=audio_id)

    except AudioDoesNotExist:
        raise HTTPException(status_code=404, detail="AudioFile not found!")


@app.put("/{audio_file_type}/{audio_id}")
def update_audio_file(audio_file_type: AudioFileType, audio_id: int,
              audio: schemas.AudioCreate, db: Session = Depends(get_db)):

    try:
        crud.update_audio_file(
            db=db, audio_file_type=audio.audioFileType, audio_id=audio_id, audio_file_metadata=audio.audioFileMetaData
        )

        return JSONResponse({
            "detail": "Audio file updated successfully!"
        })

    except UpdateError:
        raise HTTPException(status_code=500, detail="AudioFile was not updated!")

    except AudioDoesNotExist:
        raise HTTPException(status_code=404, detail="AudioFile not found!")


@app.delete("/{audio_file_type}/{audio_id}")
def delete_audio_file(audio_file_type: AudioFileType, audio_id: int, db: Session = Depends(get_db)):

    try:
        crud.delete_audio_file(db=db, audio_file_type=audio_file_type, audio_id=audio_id)
        return JSONResponse({
            "detail": "Audio file deleted successfully!"
        })

    except DeleteError:
        raise HTTPException(status_code=500, detail="AudioFile was not deleted!")

    except AudioDoesNotExist:
        raise HTTPException(status_code=404, detail="AudioFile not found!")

