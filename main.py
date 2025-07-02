from fastapi import FastAPI
from ws.voice import router as voice_router

app = FastAPI()

app.include_router(voice_router) 