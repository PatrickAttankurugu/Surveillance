from fastapi import (
    APIRouter, 
    BackgroundTasks
)
from models.schemas import (
    counter as counter_schemas
)


router = APIRouter()


@router.post(
    path="/start", 
    response_model=counter_schemas.CounterSuccessResponse
)
def start(
    background_tasks: BackgroundTasks,
    stream_id: str
):
    """
    Starts a video stream for processing
    """
    return {
        "message": "Stream started successfully"
    }
    
    
@router.post(
    path="/stop", 
    response_model=counter_schemas.CounterSuccessResponse
)
def stop(
    background_tasks: BackgroundTasks,
    stream_id: str
):
    """
    Stops a video stream from processing
    """
    return {
        "message": "Stream stopped successfully"
    }