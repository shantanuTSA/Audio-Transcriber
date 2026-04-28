from fastapi import FastAPI
from app.routes import transcribe

app = FastAPI()

app.include_router(transcribe.router)