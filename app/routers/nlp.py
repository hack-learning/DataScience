from typing import List

from fastapi import Depends, APIRouter, HTTPException

from .. import schemas, analyzer


router = APIRouter()


@router.get("/analyzer/", response_model=schemas.Dashboard)
async def get_dashboard():
    return analyzer.calculate_dashboard()