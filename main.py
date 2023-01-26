from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engineio.payload import Payload
import config
from routers import video, counter, emotion


# instantiate application
app = FastAPI(title=config.APP_NAME, version=config.APP_VERSION)


# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ALLOW_ORIGINS,
    allow_credentials=config.CORS_ALLOW_CREDENTIALS,
    allow_methods=config.CORS_ALLOW_METHODS,
    allow_headers=config.CORS_ALLOW_HEADERS
)


# add routers
app.include_router(video.router, prefix="/video", tags=["video"])
app.include_router(counter.router, prefix="/counter", tags=["counter"])
app.include_router(emotion.router, prefix="/emotion", tags=["detector"])
