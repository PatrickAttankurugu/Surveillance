from pydantic import BaseModel, Field
from fastapi import File, UploadFile
from models.schemas.extras import SuccessResponse


class UploadLink(BaseModel):
    stream_name: str = Field(
        ...,
        title="Stream Name",
        description="The name of the video stream",
        min_length=1
    )
    link: str = Field(
        ...,
        title="Stream Link",
        description="The URL for the video stream",
        min_length=1
    )
    
    
class UploadVideo(BaseModel):
    stream_name: str = Field(
        ...,
        title="Stream Name",
        description="The name of the video stream",
        min_length=1
    )
    video_file: UploadFile = Field(
        ...,
        title="Video File",
        description="The video file"
    )
    
    
class StreamRecord(BaseModel):
    id: int = Field(
        ...,
        title="Record ID",
        description="Database assigned ID"
    )
    name: str = Field(
        ...,
        title="Name of Stream",
        description="The filename of the video stream"
    )
    type: str = Field(
        ...,
        title="Type of Stream",
        description="The type of stream (local or remote)"
    )
    path_or_link: str = Field(
        ...,
        title="Path or Link",
        description="The path or link to the video"
    )


class UploadSuccessResponse(SuccessResponse):
    pass


class UploadSuccessResponseWithData(SuccessResponse):
    data: list[tuple]