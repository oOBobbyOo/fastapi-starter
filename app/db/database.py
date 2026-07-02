"""数据库连接管理。

提供带重试机制的数据库连接初始化、资源释放与会话依赖注入。
"""

import asyncio
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import get_logger
from app.db.session import async_session, engine

logger = get_logger(__name__)


async def init_db(
    max_retries: int = settings.DATABASE_MAX_RETRIES,
    retry_interval: int = settings.DATABASE_RETRY_INTERVAL,
) -> None:
    """初始化数据库连接，带重试机制。

    在 lifespan 启动阶段调用，验证数据库是否可达。
    若连接失败，将按 interval 秒间隔重试，直到 max_retries 次。

    Args:
        max_retries: 最大重试次数，默认 5。
        retry_interval: 重试间隔（秒），默认 3。

    Raises:
        ConnectionError: 所有重试均失败时抛出。
    """
    for attempt in range(1, max_retries + 1):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("✅ 数据库连接成功。")
            return
        except Exception as exc:
            logger.warning(
                "⚠️ 数据库连接失败 (第 %d/%d 次): %s",
                attempt,
                max_retries,
                exc,
            )
            if attempt < max_retries:
                await asyncio.sleep(retry_interval)
            else:
                logger.error("❌ 数据库连接失败, 已达最大重试次数。")
                msg = f"无法连接到数据库: {exc}"
                raise ConnectionError(msg) from exc


async def close_db() -> None:
    """释放数据库引擎资源。

    在 lifespan 关闭阶段调用。
    """
    await engine.dispose()
    logger.info("🔌 数据库连接已释放。")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话的依赖注入。

    用法:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...

    自动管理事务: 成功提交，异常回滚。
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
