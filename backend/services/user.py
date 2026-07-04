from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging
from schemas.user import UserCreate, UserPageResponse, UserUpdate
from models.user import User
from core.security import get_password_hash, verify_password, create_access_token
from DAO import user as crud

logger = logging.getLogger(__name__)


async def create_user(user_data: UserCreate, db: AsyncSession):
    logger.info("创建用户请求: username=%s", user_data.username)

    existing = await crud.get_user_by_username(user_data.username, db)
    if existing:
        logger.warning("用户已存在: username=%s", user_data.username)
        raise HTTPException(
            status_code=400,
            detail="用户已经存在"
        )

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        password=hashed_password,
        role=user_data.role,
        email=user_data.email
    )

    await crud.create_user(new_user, db)
    await db.commit()
    await db.refresh(new_user)

    logger.info("用户创建成功: id=%s", new_user.id)
    return new_user


async def login_user(email: str, password: str, db: AsyncSession):
    logger.info("用户登录请求: email=%s", email)

    # 存在 user == User 对象，不存在 user == None
    user = await crud.get_user_by_email(email, db)
    if not user:
        logger.warning("用户不存在: email=%s", email)
        raise HTTPException(
            status_code=401,
            detail="非法身份"
        )

    if not verify_password(password, user.password):
        logger.warning("密码错误: email=%s", email)
        raise HTTPException(
            status_code=401,
            detail="非法身份"
        )

    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role}
    )

    logger.info("用户登录成功: email=%s", email)
    return {
        "token": access_token,
        "user_info": user
    }


async def get_user_list(page: int, page_size: int, db: AsyncSession):
    total, items = await crud.get_user_list(page, page_size, db)
    return UserPageResponse(
        total=total,
        items=items
    )


async def delete_user(user_id: int, db: AsyncSession):
    await crud.delete_user(user_id, db)
    await db.commit()
    return {
        "code": 200,
        "message": "删除成功"
    }


async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession):
    logger.info("更新用户信息请求：user_id=%s", user_id)
    
    user = await crud.get_user_by_id(user_id, db)
    if not user:
        logger.warning("用户不存在：user_id=%s", user_id)
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    
    # 只允许更新 email 和 role
    update_data = user_data.model_dump(exclude_unset=True)
    if "email" in update_data:
        user.email = update_data["email"]
    if "role" in update_data:
        user.role = update_data["role"]
    
    await db.commit()
    await db.refresh(user)
    
    logger.info("用户信息更新成功：user_id=%s", user_id)
    return user


async def get_user_by_id(user_id: int, db: AsyncSession):
    logger.info("获取用户信息请求：user_id=%s", user_id)
    
    user = await crud.get_user_by_id(user_id, db)
    if not user:
        logger.warning("用户不存在：user_id=%s", user_id)
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    
    return user


async def change_password(user_id: int, old_password: str, new_password: str, db: AsyncSession):
    logger.info("修改密码请求：user_id=%s", user_id)
    
    user = await crud.get_user_by_id(user_id, db)
    if not user:
        logger.warning("用户不存在：user_id=%s", user_id)
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    
    if not verify_password(old_password, user.password):
        logger.warning("原密码错误：user_id=%s", user_id)
        raise HTTPException(
            status_code=400,
            detail="旧密码错误"
        )
    
    user.password = get_password_hash(new_password)
    await db.commit()
    
    logger.info("密码修改成功：user_id=%s", user_id)
    return {"code": 200, "message": "密码修改成功"}
