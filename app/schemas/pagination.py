"""
分页相关的 Pydantic 模型。

包含分页请求参数和分页响应结构，供所有需要分页的端点复用。
"""

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """
    分页请求参数。

    作为 FastAPI 依赖注入使用，自动从 Query 参数解析。
    提供 skip 属性，方便服务层直接使用偏移量。
    """

    page: int = Field(default=1, ge=1, description="页码 (从 1 开始)")
    page_size: int = Field(default=20, ge=1, le=100, description="每页大小 (1-100)")

    @property
    def skip(self) -> int:
        """转换为数据库偏移量(skip)，供服务层使用。"""
        return (self.page - 1) * self.page_size


class PaginatedResponse[T](BaseModel):
    """
    通用分页响应结构。

    泛型参数 T 为列表项的类型（如 UserResponse）。

    Attributes:
        items: 当前页数据列表
        total: 总记录数
        page: 当前页码
        page_size: 每页大小
        has_more: 是否还有更多数据
        total_pages: 总页数
    """

    items: list[T] = Field(..., description="当前页数据列表")
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")
    has_more: bool = Field(..., description="是否还有更多数据")
    total_pages: int = Field(..., description="总页数")

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedResponse[T]":
        """
        工厂方法：自动计算分页元数据。

        Args:
            items: 当前页数据
            total: 总记录数
            page: 当前页码
            page_size: 每页大小

        Returns:
            完整的分页响应对象
        """
        # 计算总页数（向上取整）
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        has_more = page < total_pages

        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            has_more=has_more,
            total_pages=total_pages,
        )
