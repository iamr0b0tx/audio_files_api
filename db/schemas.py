from datetime import datetime
from typing import Union, Optional, Literal, NewType

from pydantic import BaseModel, constr, conint, conlist

AudioFileType = NewType('AudioFileType', Literal['song', 'podcast', 'audiobook'])


class AudioSchema(BaseModel):
    id: int
    duration: conint(gt=0)
    uploaded_time: datetime


class SongSchema(AudioSchema):
    name: constr(min_length=1, max_length=100)

    class Config:
        orm_mode = True


class PodcastSchema(AudioSchema):
    name: constr(min_length=1, max_length=100)
    host: constr(min_length=1, max_length=100)
    participants: Optional[conlist(constr(min_length=1, max_length=100), min_items=0, max_items=10)] = []

    class Config:
        orm_mode = True


class AudiobookSchema(AudioSchema):
    title: constr(min_length=1, max_length=100)
    author: constr(min_length=1, max_length=100)
    narrator: constr(min_length=1, max_length=100)

    class Config:
        orm_mode = True


class SongCreateSchema(BaseModel):
    name: constr(min_length=1, max_length=100)
    duration: conint(gt=0)


class PodcastCreateSchema(BaseModel):
    name: constr(min_length=1, max_length=100)
    duration: conint(gt=0)
    host: constr(min_length=1, max_length=100)
    participants: Optional[conlist(constr(min_length=1, max_length=100), min_items=0, max_items=10)] = []


class AudiobookCreateSchema(BaseModel):
    title: constr(min_length=1, max_length=100)
    author: constr(min_length=1, max_length=100)
    narrator: constr(min_length=1, max_length=100)
    duration: conint(gt=0)


AudioTypeSchemas = Union[SongSchema, PodcastSchema, AudiobookSchema]


class AudioCreate(BaseModel):
    audioFileType: AudioFileType
    audioFileMetaData: Union[SongCreateSchema, PodcastCreateSchema, AudiobookCreateSchema]


