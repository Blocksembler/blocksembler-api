from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schema.tan import TanRead
from app.db.database import get_session
from app.db.model.tan import Tan

router = APIRouter(
    prefix="/tans",
    tags=["tan"],
)


@router.get("/{code}",
            response_model=TanRead,
            status_code=status.HTTP_200_OK)
async def get_tan_code(code: str, session: AsyncSession = Depends(get_session)) -> TanRead:
    statement = select(Tan).where(Tan.code == code)
    result = await session.execute(statement)
    tan = result.scalars().first()

    if not tan:
        raise HTTPException(status_code=404, detail="Item not found")

    return TanRead(**tan.to_dict())
