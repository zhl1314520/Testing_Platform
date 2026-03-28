from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# 数据库连接地址
DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/dbdbdb?charset=utf8mb4"

# 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=False,     # 不输出 SQL 日志
    pool_size=10,       # 连接池大小
    max_overflow=20,        # 最大溢出连接数
    pool_recycle=1800,      # 池回收时间
)

# 创建 session 工厂
async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

"""
依赖注入
"""
# 获取数据库 session
async def get_db():
    async with async_session_factory() as session:
        yield session