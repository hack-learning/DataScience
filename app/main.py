from typing import List

from fastapi import Depends, FastAPI

from .routers import nlp


app = FastAPI(title="Master Path API",
    description="REST API which through multiple endpoints support Master Learning path app.",
    version="1.0",)
    
app.include_router(
    nlp.router,
    prefix="/api/v1",
    tags=["Dashboard Endpoints"],
    responses={404: {"description": "Not found"}},
)

@app.get("/", tags=["API Root"])
def welcome():
    return {"Welcome to Master Path Data Science API"}