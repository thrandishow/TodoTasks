from fastapi import APIRouter,status
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user():

