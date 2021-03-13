from datetime import datetime
from typing import Union, Optional, Literal, NewType, List, Tuple

from pydantic import BaseModel, constr, conint, conlist, validator, root_validator

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
    participants: conlist(constr(min_length=1, max_length=100), min_items=0, max_items=10)


class AudiobookCreateSchema(BaseModel):
    title: constr(min_length=1, max_length=100)
    author: constr(min_length=1, max_length=100)
    narrator: constr(min_length=1, max_length=100)
    duration: conint(gt=0)


AudioTypeSchemas = Union[PodcastSchema, AudiobookSchema, SongSchema]
AudioCreateTypeSchemas = Union[PodcastCreateSchema, AudiobookCreateSchema, SongCreateSchema]

type_to_create_schema_map = {
    "song": SongCreateSchema,
    "podcast": PodcastCreateSchema,
    "audiobook": AudiobookCreateSchema
}


class AudioCreate(BaseModel):
    audioFileType: AudioFileType
    audioFileMetaData: AudioCreateTypeSchemas

    @root_validator
    def validate_audio_file_metadata_type(cls, values):
        audio_file_type = values.get("audioFileType")
        audio_file_metadata = values.get("audioFileMetaData")

        expected_type = type_to_create_schema_map.get(audio_file_type)
        assert isinstance(audio_file_metadata, expected_type) is True, "Invalid data not matching the audio file type"
        return values
