from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# 创建异步数据库引擎
engine = create_async_engine(
    settings.DATABASE_URL,  # 数据库连接 URL
    echo=settings.DATABASE_ECHO,  # 是否开启 SQL 语句回显 (Echo)
    pool_size=settings.DATABASE_POOL_SIZE,  # 连接池大小 (Pool Size)
    max_overflow=settings.DATABASE_MAX_OVERFLOW,  # 最大溢出连接数 (Max Overflow)
    pool_pre_ping=True,  # 连接池预检活机制 (Pool Pre-Ping)
    # 连接回收时间 (秒)
    # 强制在连接空闲达到指定时间后将其回收并重建。
    # 对于 MySQL，建议设置为小于 8 小时的值，例如 3600 (1小时) 或 1800 (半小时)。
    # 对于 PostgreSQL，通常不需要设置，因为 PG 不会主动杀空闲连接。
    # pool_recycle=1800,
)

# 创建异步 Session 工厂
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话的依赖注入。

    用法:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...

    自动管理事务: 成功提交，异常回滚。
    """

    # 使用 async_session 生成一个 session 实例
    async with async_session() as session:
        try:
            # 将 session 注入到路由函数中
            yield session
            # 路由函数正常执行完毕，自动提交事务
            await session.commit()
        except Exception:
            # 发生异常，自动回滚事务
            await session.rollback()
            raise
        finally:
            # 确保 session 被正确关闭，归还连接到连接池
            await session.close()
