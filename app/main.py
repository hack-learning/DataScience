from typing import List

from fastapi import Depends, FastAPI

#from .routers import


app = FastAPI(title="Master Path API",
    description="REST API which through multiple endpoints support Master Learning path app.",
    version="1.0",)
    


@app.get("/", tags=["API Root"])
def welcome():
    return {"Welcome to Master Path Data Science API"}