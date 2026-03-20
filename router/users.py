from fastapi import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud import users
from crud.users import get_user_by_email
from schema.users import UserInfo

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@router.post("/register")
async def register(user_info: UserInfo, db: AsyncSession = Depends(get_db)):
    # 判断用户是否存在
    is_existing_user = await users.get_user_by_email(user_info.email, db)
    if is_existing_user:
        raise HTTPException(status_code=400, detail="该用户已存在")
    user = await users.create_user(user_info, db)

    return {"message": "register"}


@router.post("/login")
async def login():
    return {"message": "login"}