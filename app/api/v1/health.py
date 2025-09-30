from fastapi import APIRouter, HTTPException, status

from app.database import get_db

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("/")
async def health_check() -> dict:
    try:
        db = await get_db()
        await db.command("ping")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return {"status": "ok"}
