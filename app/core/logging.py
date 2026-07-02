"""
日志配置。

提供结构化日志设置，支持 JSON 格式输出（生产环境）和彩色控制台输出（开发环境）。
"""

import logging
import sys

from app.core.config import settings


def setup_logging() -> None:
    """配置应用日志。"""
    level = getattr(logging, settings.LOG_LEVEL, logging.INFO)

    if settings.is_production:
        # 生产环境: JSON 结构化日志
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                '{"time": "%(asctime)s", "level": "%(levelname)s", '
                '"name": "%(name)s", "message": "%(message)s"}'
            )
        )
    else:
        # 开发环境: 彩色可读日志
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] %(levelname)-8s %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    # 移除已有 handler 避免重复
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # 抑制第三方库的过细日志
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.DATABASE_ECHO else logging.WARNING
    )


def get_logger(name: str) -> logging.Logger:
    """获取指定模块的 logger 实例。

    替代分散在各模块中的 logging.getLogger(__name__)，
    统一 logger 获取方式，方便后续扩展（如注入上下文）。
    """
    return logging.getLogger(name)
