from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from model.users import Admin, Developer, Tester
from schema.users import UserInfo
from utils import pwd_security


# 根据 Email 查询用户(通用)
async def get_user_by_email(email: str, db: AsyncSession):
    for model in [Admin, Developer, Tester]:
        stmt = select(model).where(model.email == email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if user:
            return user
    return None

# 创建用户
async def create_user(user_info: UserInfo, db: AsyncSession):
    # 加密
    security_password = pwd_security.set_hash_password(user_info.password)
    user = UserInfo(email=user_info.email, password=security_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user