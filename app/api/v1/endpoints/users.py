"""
Users 端点。

提供 /Users 资源的 CRUD 操作。
"""

from uuid import UUID

from fastapi import APIRouter

from app.api.deps import DBSession, Pagination
from app.api.v1.schemas.users import UserCreate, UserResponse, UserUpdate
from app.schemas.pagination import PaginatedResponse
from app.services.user import user_service
from app.utils.exceptions import NotFoundException

router = APIRouter()


@router.get("/{user_id}", response_model=UserResponse, summary="获取用户")
async def get_user(user_id: UUID, db: DBSession) -> UserResponse:
    """根据 User ID 获取用户详情"""

    user = await user_service.get(db, obj_id=user_id)
    if not user:
        raise NotFoundException(
            detail="User not found",
        )
    return UserResponse.model_validate(user)


@router.get("/", response_model=PaginatedResponse[UserResponse], summary="分页获取用户列表")
async def list_users(
    pagination: Pagination,
    db: DBSession,
) -> PaginatedResponse[UserResponse]:
    """分页查询用户列表"""

    users, total = await user_service.get_multi_page(
        db,
        skip=pagination.skip,
        limit=pagination.page_size,
    )

    items = [UserResponse.model_validate(u) for u in users]

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.post("/", response_model=UserResponse, summary="创建用户")
async def create_user(user_in: UserCreate, db: DBSession) -> UserResponse:
    """创建新用户"""

    user = await user_service.create(db, obj_in=user_in)
    await db.commit()

    return UserResponse.model_validate(user)


@router.patch("/{user_id}", response_model=UserResponse, summary="更新用户")
async def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    db: DBSession,
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
    db: DBSession,
) -> None:
    """删除用户"""

    user = await user_service.delete(db, obj_id=user_id)
    if not user:
        raise NotFoundException(
            detail="User not found",
        )
    await db.commit()
