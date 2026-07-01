"""
Items 端点。

提供 /items 资源的 CRUD 操作。
"""

from fastapi import APIRouter, HTTPException, status

router = APIRouter()

# 模拟数据存储
_items_db: dict[int, dict[str, object]] = {
    1: {"id": 1, "name": "Item One", "price": 9.99},
    2: {"id": 2, "name": "Item Two", "price": 19.99},
}


@router.get("/{item_id}", summary="获取单个物品")
async def get_item(item_id: int) -> dict[str, object]:
    """根据 ID 获取物品详情。"""
    item = _items_db.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return item
