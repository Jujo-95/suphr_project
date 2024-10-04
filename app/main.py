from fastapi import FastAPI
from app.api import endpoints
from app.db.init_db import init_db



def lifespan():
    init_db()

app = FastAPI(lifespan=lifespan())

app.include_router(endpoints.router)