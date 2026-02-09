from fastapi import APIRouter
from starlette import status

router = APIRouter(
    prefix='/health',
    tags=['health']
)


@router.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    return {
        "health": "ok"
    }
