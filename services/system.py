from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging
from schemas.system import SystemCreate
from models.system import System
from crud import system as crud

# 日志
logger = logging.getLogger(__name__)

# 创建系统（业务逻辑）
async def create_system(system_data: SystemCreate, db: AsyncSession):
    # 日志：记录请求
    logger.info("创建系统请求: name=%s", system_data.name)

    # 1. 判断是否已存在
    existing = await crud.get_system_by_name(system_data.name, db)
    if existing:
        logger.warning("系统已存在: name=%s", system_data.name)
        raise HTTPException(
            status_code=400,
            detail="SYSTEM_ALREADY_EXISTS"
        )

    # 2. 构造 ORM 对象
    new_system = System(
        name=system_data.name,
        description=system_data.description
    )

    # 3. 入库
    await crud.create_system(new_system, db)

    # 4. 提交事务
    await db.commit()

    # 5. 刷新对象（获取最新数据）
    await db.refresh(new_system)

    # 日志：记录成功
    logger.info("系统创建成功: id=%s", new_system.id)

    return new_system