"""
API 依赖注入。

提供路由处理器通过 Depends() 注入的公共依赖，
如分页参数、当前用户、数据库会话等。
"""

from typing import Annotated, Any

from fastapi import Depends, Header, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.database import get_db
from app.schemas.pagination import PaginationParams


# ---- 分页 ----
async def pagination_params(
    page: int = Query(1, ge=1, description="页码 (从 1 开始)"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小 (1-100)"),
) -> PaginationParams:
    """
    分页参数依赖。

    自动从 Query 参数解析并构造 PaginationParams 实例。
    """
    return PaginationParams(page=page, page_size=page_size)


# ---- 认证 ----
async def get_current_user(
    authorization: str = Header(..., description="Bearer <token>"),
) -> dict[str, Any]:
    """
    从 Authorization 头中提取并验证当前用户。

    用法:
        @router.get("/me")
        async def me(user: dict = Depends(get_current_user)):
            return user
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token = authorization.removeprefix("Bearer ")

    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return payload


# ---- 类型别名：简化路由签名 ----
Pagination = Annotated[PaginationParams, Depends(pagination_params)]
DBSession = Annotated[AsyncSession, Depends(get_db)]
