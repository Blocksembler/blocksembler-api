import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import health, logging, tan

origins = os.environ.get("BLOCKSEMBLER_ORIGINS", "*").split(',')
BASE_URL = os.environ.get('BLOCKSEMBLER_API_BASE_URL', '')

if os.environ.get('DEBUG', 'true').lower() == 'true':
    app = FastAPI(root_path=BASE_URL)
else:
    app = FastAPI(root_path=BASE_URL, docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tan.router)
app.include_router(health.router)
app.include_router(logging.router)
