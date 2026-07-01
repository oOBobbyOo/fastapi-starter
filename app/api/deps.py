"""
API 依赖注入。

提供路由处理器通过 Depends() 注入的公共依赖，
如数据库会话、当前用户、分页参数等。
"""

from fastapi import Query

# ---- 分页 ----


async def pagination_params(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数上限"),
) -> dict[str, int]:
    """通用分页参数。"""
    return {"skip": skip, "limit": limit}
