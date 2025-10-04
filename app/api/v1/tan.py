from typing import Any

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models.tan import TAN

router = APIRouter(
    prefix="/tan",
    tags=["tan"],
)


@router.get("/{code}",
            response_model=TAN,
            status_code=status.HTTP_200_OK)
async def get_tan_code(code: str, session: AsyncSession = Depends(get_session)) -> Any:
    statement = select(TAN).where(TAN.code == code)
    result = await session.execute(statement)
    tan = result.scalars().first()

    if not tan:
        raise HTTPException(status_code=404, detail="Item not found")

    return tan
