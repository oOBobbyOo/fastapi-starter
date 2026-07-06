"""
API v1 路由聚合。

将所有 /api/v1/ 下的模块路由统一注册。
"""

from fastapi import APIRouter

from app.api.v1.endpoints import items, users

api_router = APIRouter()

api_router.include_router(items.router, prefix="/items", tags=["Items"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
