from fastapi import FastAPI

from app.db import Base, engine
from app.routers import users
import app.models
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)


@app.on_event("startup")
def on_startup():
    # Crea las tablas si no existen (y el fichero sqlite)
    Base.metadata.create_all(bind=engine)


# Routers
app.include_router(users.router)


@app.get("/", tags=["health"])
def read_root():
    return {"message": "Soy una api voladora no identifiada"}
