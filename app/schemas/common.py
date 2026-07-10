"""
通用响应结构。

提供统一的 API 响应格式，保证所有接口返回风格一致。
"""

from pydantic import BaseModel, Field


class SuccessResponse[T](BaseModel):
    """
    统一成功响应结构。

    用于包装需要返回额外元数据的接口（如分页、统计等）。

    Example:
        {
            "code": 0,
            "message": "success",
            "data": {...}
        }
    """

    code: int = Field(default=0, description="状态码 0 表示成功")
    message: str = Field(default="success", description="响应消息")
    data: T | None = Field(default=None, description="响应数据")
