from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.routers import api_router

NUM_OPTIONS = 3 # Define the number of options for multiple choice questions
MODEL = "gpt-3.5-turbo"


app = FastAPI(
    title = settings.PROJECT_NAME,
    version = settings.PROJECT_VERSION
)

origins = [
    'https://scorelab.pe'
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["GET", "POST", "OPTIONS"],
    allow_headers = ["*"]
)

app.include_router(api_router, prefix='/api')

