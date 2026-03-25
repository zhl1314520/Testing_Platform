"""
依赖注入
"""
from core.db import async_session_factory

# 获取数据库 session
async def get_db():
    async with async_session_factory() as session:
        yield session