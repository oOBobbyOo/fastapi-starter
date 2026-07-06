"""
API 依赖注入。

提供路由处理器通过 Depends() 注入的公共依赖，
如分页参数、当前用户等。
"""

from typing import Any

from fastapi import Header, HTTPException, Query, status

from app.core.security import decode_token


# ---- 分页 ----
async def pagination_params(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数上限"),
) -> dict[str, int]:
    """通用分页参数。"""
    return {"skip": skip, "limit": limit}


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
