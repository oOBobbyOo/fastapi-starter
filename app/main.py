"""
FastAPI 应用入口。

创建 FastAPI 实例、注册中间件、挂载路由和静态文件。
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.db.database import close_db, init_db
from app.utils.exception_handlers import register_exception_handlers

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    应用生命周期管理。

    启动时初始化资源（数据库连接池、Redis 等），
    关闭时优雅释放资源。
    """

    # 设置日志
    setup_logging()

    # ================= 启动阶段 (Startup) =================
    logger.info("🚀 应用程序正在启动...")

    # 初始化数据库
    await init_db()

    yield  # <--- 应用运行中，处理 HTTP 请求

    # ================= 关闭阶段 (Shutdown) =================
    logger.info("🛑 应用程序正在关闭...")

    # 释放数据库资源
    await close_db()

    logger.info("👋 应用程序关闭完成.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ---- 注册异常处理器 ----
register_exception_handlers(app)

# ---- 中间件注册 ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- 路由注册 ----
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# ---- 静态文件 ----
app.mount("/static", StaticFiles(directory="static"), name="static")


# Health check endpoint
@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy"}
