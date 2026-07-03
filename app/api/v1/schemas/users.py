"""
Users Schema。

定义用户资源的请求/响应 Pydantic 模型。
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """用户基础模型。"""

    name: str = Field(..., min_length=2, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")


class UserCreate(UserBase):
    """创建用户请求模型（注册）。"""

    password: str = Field(..., min_length=8, description="用户密码")


class UserUpdate(BaseModel):
    """更新用户请求模型。"""

    name: str | None = Field(None, min_length=2, max_length=50, description="新用户名")
    email: EmailStr | None = Field(None, description="新邮箱")
    password: str | None = Field(None, min_length=8, description="新密码")


class UserResponse(UserBase):
    """
    用户响应模型。
    用于接口返回用户信息。
    """

    id: int = Field(..., description="用户唯一 ID")

    # 安全设计：响应模型中坚决不包含 password 字段，防止密码泄露

    model_config = ConfigDict(from_attributes=True)
