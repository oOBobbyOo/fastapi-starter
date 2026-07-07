"""
Users 端点。

提供 /Users 资源的 CRUD 操作。
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.users import UserCreate, UserResponse, UserUpdate
from app.db.database import get_db
from app.services.user import user_service
from app.utils.exceptions import NotFoundException

router = APIRouter()


@router.get("/{user_id}", response_model=UserResponse, summary="获取用户")
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> UserResponse:
    """根据 User ID 获取用户详情"""

    user = await user_service.get(db, obj_id=user_id)
    if not user:
        raise NotFoundException(
            detail="User not found",
        )
    return UserResponse.model_validate(user)


@router.get("/", response_model=list[UserResponse], summary="获取用户列表")
async def get_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
) -> list[UserResponse]:
    """分页查询用户列表"""

    users = await user_service.get_multi(db, skip=skip, limit=limit)
    return [UserResponse.model_validate(user) for user in users]


@router.post("/", response_model=UserResponse, summary="创建用户")
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    """创建新用户"""

    user = await user_service.create(db, obj_in=user_in)
    await db.commit()

    return UserResponse.model_validate(user)


@router.patch("/{user_id}", response_model=UserResponse, summary="更新用户")
async def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """更新用户信息"""

    user = await user_service.get(db, obj_id=user_id)
    if not user:
        raise NotFoundException(
            detail="User not found",
        )

    user = await user_service.update(db, obj_in=user_in, db_obj=user)
    await db.commit()
    return UserResponse.model_validate(user)


@router.delete("/{user_id}", summary="删除用户")
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """删除用户"""

    user = await user_service.delete(db, obj_id=user_id)
    if not user:
        raise NotFoundException(
            detail="User not found",
        )
    await db.commit()
