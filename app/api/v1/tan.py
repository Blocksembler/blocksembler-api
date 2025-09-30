import random
import string
from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.database import get_db
from app.schemas.tan import TanCode

router = APIRouter(
    prefix="/tan",
    tags=["tan"],
)


def generate_tan(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


@router.get("/{code}",
            response_model=TanCode,
            status_code=status.HTTP_200_OK)
async def get_tan_code(code: str) -> Any:
    db = await get_db()
    result = await db.tans.find_one({'code': code})

    if not result:
        raise HTTPException(status_code=404, detail="Item not found")

    return TanCode(**result)
