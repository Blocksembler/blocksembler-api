import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("/")
async def health_check(session: AsyncSession = Depends(get_session)) -> dict:
    try:
        result = await session.execute(text("SELECT 1"))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Database connection error")

    return {"status": "ok"}
