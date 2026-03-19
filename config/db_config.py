from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# 数据库URL
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8mb4"

# 创建异步引擎
async_engine = create_async_engine(
ASYNC_DATABASE_URL,
    echo=True,  # 可选，输出sql日志
    pool_size=10,  # 可选，连接池大小
    max_overflow=20,  # 可选，连接池溢出时的最大连接数
)

# 创建异步会话工厂
async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,  # 可选，提交后不失效对象
    class_=AsyncSession,  # 使用异步会话类
)

# 依赖项，用于获取数据库会话
async def get_db():
    async with async_session_factory() as session:
        try:
            yield session           # 生成器函数，提供数据库会话
            await session.commit()  # 提交事务
        except Exception:
            await session.rollback()  # 回滚事务
            raise                      # 重新抛出异常
        finally:
            await session.close()  # 确保会话关闭