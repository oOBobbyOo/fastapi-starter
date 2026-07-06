"""
Users Schema。

定义用户资源的请求/响应 Pydantic 模型。
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """用户基础模型。"""

    username: str = Field(
        ..., min_length=2, max_length=50, title="用户名", description="用户名2-50个字符"
    )
    email: EmailStr = Field(..., title="邮箱", description="有效的邮箱地址")


class UserCreate(UserBase):
    """创建用户请求模型（注册）。"""

    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
        title="密码",
        description="密码长度8-20位",
    )


class UserUpdate(BaseModel):
    """更新用户请求模型。"""

    username: str | None = Field(None, min_length=2, max_length=50, description="新用户名")
    email: EmailStr | None = Field(None, description="新邮箱")
    password: str | None = Field(None, min_length=8, max_length=20, description="新密码")


class UserResponse(UserBase):
    """
    用户响应模型。
    用于接口返回用户信息。
    """

    id: UUID = Field(..., title="用户ID", description="UUID v4 格式的用户唯一标识符")
    created_at: datetime | None = Field(None, title="创建时间", description="用户账户的创建时间")
    updated_at: datetime | None = Field(
        None, title="更新时间", description="用户信息的最后更新时间"
    )

    # 安全设计：响应模型中坚决不包含 password 字段，防止密码泄露

    model_config = ConfigDict(from_attributes=True)
