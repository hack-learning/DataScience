from typing import List

from fastapi import Depends, APIRouter, HTTPException

from .. import schemas, news_query


router = APIRouter()


@router.get("/news")
async def get_sentiment():
    return news_query.get_news()
