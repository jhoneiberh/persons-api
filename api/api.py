"""FastAPI."""
# python
from typing import Optional
from enum import Enum
import uvicorn

# pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from pydantic import HttpUrl

# fastapi
from fastapi import FastAPI
from fastapi import status
from fastapi import Body
from fastapi import Path
from fastapi import UploadFile
from fastapi import File
from fastapi import Query
from fastapi import Form
from fastapi import Header
from fastapi import Cookie
from fastapi import HTTPException

from api.models import Location, LoginOut, Person, PersonOut
from api.routes import router as PersonRouter

app = FastAPI()

# Models


@app.get("/", tags=["Home"])
async def read_root() -> dict:
    return {
        "message": "Welcome to my notes application, use the /docs route to proceed"
    }

app.include_router(PersonRouter, prefix="/api")






