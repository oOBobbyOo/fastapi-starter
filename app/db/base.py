"""
SQLAlchemy 声明式基类。

所有 ORM 模型从此基类继承，统一管理表名和元数据。
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """SQLAlchemy 声明式基类。"""

    pass
