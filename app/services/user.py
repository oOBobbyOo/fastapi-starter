from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.users import UserCreate, UserUpdate
from app.core.security import password_hash
from app.models.user import User
from app.services.base import CRUDBase


class UserService(CRUDBase[User, UserCreate, UserUpdate]):
    """用户服务，继承通用 CRUD"""

    # ========== 自定义业务方法 ==========

    async def get_by_email(self, db: AsyncSession, *, email: str) -> User | None:
        """通过邮箱查找用户"""

        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, *, username: str) -> User | None:
        """通过用户名查找用户"""

        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    # ========== 重写基类方法（添加业务逻辑） ==========

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """创建用户时自动加密密码"""

        # 检查邮箱是否已存在
        existing = await self.get_by_email(db, email=obj_in.email)
        if existing:
            raise ValueError("邮箱已注册")

        # 检查用户名是否已存在
        existing = await self.get_by_username(db, username=obj_in.username)
        if existing:
            raise ValueError("用户名已被占用")

        # 创建用户对象，密码加密
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=password_hash(obj_in.password),
        )
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj


user_service = UserService(User)
