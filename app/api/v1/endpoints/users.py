"""
Users 端点。

提供 /Users 资源的 CRUD 操作。
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.users import UserResponse
from app.db.database import get_db
from app.services.user import user_service
from app.utils.exceptions import NotFoundException

router = APIRouter()


@router.get("/{user_id}", response_model=UserResponse, summary="获取用户")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    """根据 User ID 获取用户详情。"""

    user = await user_service.get(db, obj_id=user_id)
    if not user:
        raise NotFoundException(
            detail="User not found",
        )
    return UserResponse.model_validate(user)
