from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.system import System

# 判断项目系统是否存在
"""
ERROR:
    业务逻辑设计错（用 id 判断是否存在）
❗原因：
id 是自增主键
用户不应该传 id 来创建
id 应该由数据库生成

改进：
    使用 name 作为查询依据
"""
async def get_system_by_name(name: str, db: AsyncSession):
    stmt = select(System).where(System.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# 创建项目系统
async def create_system(system: System, db: AsyncSession):
    db.add(system)
    await db.flush()  # 刷新获取ID（不提交事务）
    return system

