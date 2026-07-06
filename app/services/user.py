from app.api.v1.schemas.users import UserCreate, UserUpdate
from app.models.user import User
from app.services.base import CRUDBase


class UserService(CRUDBase[User, UserCreate, UserUpdate]):
    """用户服务，继承通用 CRUD"""


user_service = UserService(User)
