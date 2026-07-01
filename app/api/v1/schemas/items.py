"""
Items Schema。

定义物品资源的请求/响应 Pydantic 模型。
"""

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """物品基础字段。"""

    name: str = Field(..., min_length=1, max_length=255, examples=["Widget"])
    price: float = Field(..., gt=0, examples=[9.99])


class ItemCreate(ItemBase):
    """创建物品请求体。"""

    pass


class ItemUpdate(BaseModel):
    """更新物品请求体（全部字段可选）。"""

    name: str | None = Field(None, min_length=1, max_length=255)
    price: float | None = Field(None, gt=0)


class ItemResponse(ItemBase):
    """物品响应体。"""

    id: int

    model_config = {"from_attributes": True}
