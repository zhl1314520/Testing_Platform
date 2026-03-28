from sqlalchemy import select, func
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

# 获取分页数据
async def get_system_list(page: int, page_size: int, db: AsyncSession):
    # 查询总数
    count_stmt = select(func.count()).select_from(System)       # SELECT COUNT(*) FROM system_name;
    """
    假如 上面那行返回：
        COUNT(*)
        --------
        420
        
    那么scalar() 就是获取第一行第一列的数据，即 420
    """
    total = (await db.execute(count_stmt)).scalar()

    # 查询分页数据
    stmt = (
        select(System)
        .offset((page - 1) * page_size) # 跳过前几条，实现分页
        .limit(page_size)
        .order_by(System.id.desc())
    )

    result = await db.execute(stmt)
    """
    .scalars() 会把每一行的 第一列（在 ORM 查询中，就是整个 System 对象本身）取出来。
    .all() 会将所有行收集成一个 list【】
    item就是一个列表
        如：
            [
                <System id=23 name='系统C' description='描述C'，表里其他字段。。。>,
                <System id=22 name='系统B' description='描述B'，表里其他字段。。。>,
                <System id=21 name='系统A' description='描述A'，表里其他字段。。。>,
            ]
    """
    items = result.scalars().all()

    return total, items


