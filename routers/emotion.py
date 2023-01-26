import binascii
import cv2
from fastapi import (
    APIRouter,
    Depends, 
    WebSocket,
    BackgroundTasks,
    WebSocketDisconnect
)
from models.schemas import (
    emotion as emotion_schemas
)
from models.crud import (
    video as video_crud
)
import config
from utilities.connection_manager import ConnectionManager
from utilities.image_funcs import ImageProcessor


router = APIRouter()
manager = ConnectionManager()


@router.websocket('/start', name="emotion stream")
async def start(websocket: WebSocket):
    """
    Starts processing video stream
    """
    # accept connection and add websocket to the list of connected sockets in the manager
    await manager.connect(websocket)
    
    # get the stream ID to be processed
    stream_id = await websocket.receive_text()
    
    # retrieve the record of that stream and get the link or path
    stream_data = video_crud.get_stream_by_id(stream_id=stream_id)
    link_or_path = stream_data.path_or_link if stream_data.path_or_link.startswith("http") else config.VIDEOS_BASE_PATH / stream_data.path_or_link
    
    try:
        # start capturing the frames in the video stream
        video_cap = cv2.VideoCapture(str(link_or_path))
        
        while True:
            # read the next frame
            ret, frame = video_cap.read()
            
            # if the frame is available, process it and send the resulting frame via the websocket to the client
            if ret:                
                # process the frame
                frame = ImageProcessor.detect_emotion(frame)
                
                # output_bytes is a base64 string in ascii represented in bytes
                output_bytes = ImageProcessor.pil_image_to_base64(ImageProcessor.cv2_img_to_pillow(frame))
                
                # convert a base64 string in ascii to base64 string in _bytes_
                output_bytes = binascii.a2b_base64(output_bytes)
                
                # send the processed frame to the client socket
                await manager.send_personal_bytes_message(output_bytes, websocket)
    except WebSocketDisconnect:
        # disconnect the websocket when a disconnection exception is caught
        manager.disconnect(websocket)
        
        # close the video capture
        video_cap.release()
        
        # broadcast a signal to all other open sockets that the stream had been stopped
        await manager.broadcast(f"Stream with ID={stream_id} has been stopped")
    
    
@router.post(
    path="/stop", 
    response_model=emotion_schemas.EmotionSuccessResponse
)
def stop(
    background_tasks: BackgroundTasks,
    stream_id: str
):
    """
    Stops a video stream from processing
    """
    emotion_camera = None
    
    return {
        "message": "Emotion detector stopped successfully"
    }