"""
Items 端点。

提供 /items 资源的 CRUD 操作。
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import pagination_params
from app.api.v1.schemas.items import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter()

# 模拟数据存储
_items_db: dict[int, dict[str, object]] = {
    1: {"id": 1, "name": "Item One", "price": 9.99},
    2: {"id": 2, "name": "Item Two", "price": 19.99},
}


@router.get("/", summary="获取物品列表")
async def list_items(
    pagination: dict[str, int] = Depends(pagination_params),
) -> list[ItemResponse]:
    """分页获取物品列表。"""
    items = list(_items_db.values())
    return [
        ItemResponse(**item)
        for item in items[pagination["skip"] : pagination["skip"] + pagination["limit"]]
    ]


@router.get("/{item_id}", summary="获取单个物品")
async def get_item(item_id: int) -> ItemResponse:
    """根据 ID 获取物品详情。"""
    item = _items_db.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return ItemResponse(**item)


@router.post("/", status_code=status.HTTP_201_CREATED, summary="创建物品")
async def create_item(item: ItemCreate) -> ItemResponse:
    """创建新物品。"""
    new_id = max(_items_db) + 1 if _items_db else 1
    item_data = item.model_dump()
    item_data["id"] = new_id
    _items_db[new_id] = item_data
    return ItemResponse(**item_data)


@router.put("/{item_id}", summary="更新物品")
async def update_item(item_id: int, item: ItemUpdate) -> ItemResponse:
    """更新指定物品的全部字段。"""
    if item_id not in _items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    existing = _items_db[item_id]
    existing.update(item.model_dump(exclude_unset=True))
    existing["id"] = item_id
    return ItemResponse(**existing)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除物品")
async def delete_item(item_id: int) -> None:
    """删除指定物品。"""
    if item_id not in _items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    del _items_db[item_id]
