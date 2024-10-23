from math import pi
from fastapi import FastAPI

from api import crud
import auth


app = FastAPI()
app.include_router(crud.router)
app.include_router(auth.router)

