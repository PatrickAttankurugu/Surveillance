from fastapi import (
    APIRouter, 
    BackgroundTasks, 
    Depends
)
from models.schemas import (
    video as upload_schemas
)
import config
from models.crud import (
    video as upload_crud
)
from utilities.enumerations import VideoStreamTypes
import aiofiles
import asyncio
import uuid


router = APIRouter()


@router.post(
    path="/upload/link", 
    response_model=upload_schemas.UploadSuccessResponse
)
async def upload_link(
    background_tasks: BackgroundTasks,
    data: upload_schemas.UploadLink = Depends()
):
    """
    Uploads a link to a video
    """
    data.stream_name = data.stream_name.strip().upper()
    # data.link = data.link.strip().upper()
    
    upload_crud.save_stream(data.stream_name, VideoStreamTypes.REMOTE.value, data.link)
    
    return {
        "message": "Link uploaded successfully"
    }


@router.post(
    path="/upload/video", 
    response_model=upload_schemas.UploadSuccessResponse
)
async def upload_video(
    background_tasks: BackgroundTasks,
    data: upload_schemas.UploadVideo = Depends()
):
    """
    Uploads a video
    """
    data.stream_name = data.stream_name.strip().upper()
    video_filename = str(uuid.uuid1()) + f".{data.video_file.filename.split('.')[-1]}"
    
    video_file_path = config.VIDEOS_BASE_PATH / video_filename
    async with aiofiles.open(video_file_path, "wb") as buffer:
        content = await data.video_file.read()
        await buffer.write(content)
        
    upload_crud.save_stream(data.stream_name, VideoStreamTypes.LOCAL.value, video_filename)
        
    return {
        "message": "Video uploaded successfully"
    }
    
    
@router.post(
    path="/upload/view-all", 
    response_model=upload_schemas.UploadSuccessResponseWithData
)
async def view_all_videos(
    background_tasks: BackgroundTasks
):
    """
    View all videos
    """
    data = upload_crud.get_all_streams()
        
    return {
        "message": "Video uploaded successfully",
        "data": data
    }