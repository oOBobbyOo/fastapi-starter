"""
通用 CRUD 服务基类。

提供可复用的数据库操作方法，业务服务继承此类实现定制逻辑。
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel
from sqlalchemy import ColumnElement, Select, func, insert, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm.interfaces import LoaderOption

from app.db.base import Base


class CRUDBase[ModelType: Base, CreateSchemaType: BaseModel, UpdateSchemaType: BaseModel]:
    """
    CRUD 基类。

    Usage:
        class ItemService(CRUDBase[Item, ItemCreate, ItemUpdate]):
            ...

        # 自定义排序示例
        class ItemService(CRUDBase[Item, ItemCreate, ItemUpdate]):
            def __init__(self):
                super().__init__(Item, default_order_by=Item.created_at.desc())
    """

    def __init__(
        self,
        model: type[ModelType],
        *,
        default_order_by: ColumnElement[Any] | None = None,
    ):
        """
        初始化 CRUD 服务。

        Args:
            model: SQLAlchemy ORM 模型类，如 User、Item 等
            default_order_by: 默认排序字段，不传则使用模型主键升序
        """
        self.model = model
        self.default_order_by = default_order_by

    @cached_property
    def _pk_column(self) -> ColumnElement[Any]:
        """动态获取模型的主键列，用于默认排序和查询。（首次访问时通过 inspect 获取并缓存）。"""

        mapper = inspect(self.model)
        primary_keys = mapper.primary_key
        if not primary_keys:
            raise ValueError(f"Model {self.model.__name__} has no primary key defined")
        return primary_keys[0]

    @property
    def _order_by(self) -> ColumnElement[Any]:
        """默认排序字段：用户传入的 > 模型主键。"""

        return self.default_order_by or self._pk_column

    def _apply_options(
        self, stmt: Select[Any], options: Sequence[LoaderOption] | None
    ) -> Select[Any]:
        """应用关联预加载选项到查询语句。"""

        if options:
            return stmt.options(*options)
        return stmt

    def _apply_filters(
        self, stmt: Select[Any], filters: Sequence[ColumnElement[bool]] | None
    ) -> Select[Any]:
        """应用过滤条件到查询语句。"""

        if filters:
            return stmt.where(*filters)
        return stmt

    async def get(
        self,
        db: AsyncSession,
        obj_id: Any,
        *,
        options: Sequence[LoaderOption] | None = None,
    ) -> ModelType | None:
        """
        根据主键 ID 查询单条记录。

        Args:
            db: 异步数据库会话
            obj_id: 主键值（支持 int、UUID 等任意类型）
            options: 可选的关联预加载选项，如 [selectinload(Item.owner)]

        Returns:
            匹配的记录对象，不存在则返回 None
        """
        stmt = select(self.model).where(self._pk_column == obj_id)
        stmt = self._apply_options(stmt, options)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 20,
        filters: Sequence[ColumnElement[bool]] | None = None,
        options: Sequence[LoaderOption] | None = None,
        order_by: ColumnElement[Any] | None = None,
    ) -> list[ModelType]:
        """
        分页查询多条记录。

        注意：默认按主键 ID 升序排序，保证分页结果稳定。

        Args:
            db: 异步数据库会话
            skip: 跳过的记录数（偏移量），默认 0
            limit: 返回的最大记录数，默认 20
            filters: 可选的过滤条件列表，如 [Item.is_active == True]
            options: 可选的关联预加载选项
            order_by: 自定义排序字段，覆盖默认排序

        Returns:
            符合条件的模型对象列表
        """
        stmt = select(self.model)
        stmt = self._apply_filters(stmt, filters)
        stmt = self._apply_options(stmt, options)
        stmt = stmt.order_by(order_by or self._order_by).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def count(
        self,
        db: AsyncSession,
        *,
        filters: Sequence[Any] | None = None,
    ) -> int:
        """
        统计符合条件的记录总数（分页必备）。

        Args:
            db: 异步数据库会话
            filters: 可选的过滤条件列表

        Returns:
            记录总数
        """
        stmt = select(func.count()).select_from(self.model)
        stmt = self._apply_filters(stmt, filters)
        result = await db.execute(stmt)
        return result.scalar_one()

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        """
        创建新记录。

        流程：
            1. 将 Pydantic Schema 转换为 ORM 模型实例
            2. 添加到 Session
            3. flush 到数据库（生成 SQL INSERT，但不提交事务）
            4. refresh 刷新对象，获取数据库生成的字段（如 id、created_at）

        Args:
            db: 异步数据库会话
            obj_in: 创建数据的 Pydantic Schema 实例

        Returns:
            创建后的 ORM 模型对象（已包含数据库生成的字段）
        """
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def bulk_create(
        self,
        db: AsyncSession,
        *,
        objs_in: list[CreateSchemaType],
        return_objects: bool = True,
    ) -> list[ModelType] | None:
        """
        批量创建记录。

        使用 core INSERT ... RETURNING 实现高性能批量插入，单条 SQL 完成，
        避免 ORM add_all 的逐条跟踪与逐条 refresh 开销。

        Args:
            db: 异步数据库会话
            objs_in: 创建数据的 Pydantic Schema 列表
            return_objects: 是否返回完整对象列表

        Returns:
            创建后的 ORM 模型对象列表（已包含数据库生成的字段）
        """

        if not objs_in:
            return [] if return_objects else None

        stmt = insert(self.model)
        if return_objects:
            stmt = stmt.returning(self.model)

        data = [obj.model_dump() for obj in objs_in]
        result = await db.execute(stmt, data)

        if return_objects:
            return list(result.scalars().all())
        return None

    async def update(
        self,
        db: AsyncSession,
        *,
        obj_in: UpdateSchemaType | dict[str, Any],
        db_obj: ModelType,
    ) -> ModelType:
        """
        更新已有记录。

        支持两种输入格式：
            - Pydantic Schema：使用 exclude_unset=True，只更新用户明确传入的字段
            - dict：直接更新字典中的所有键值对

        注意：
            - db_obj 必须来自同一 Session 的查询结果（处于 persistent 状态）
            - 无需再次 db.add()，直接修改属性后 flush 即可

        Args:
            db: 异步数据库会话
            db_obj: 待更新的 ORM 模型对象（需从数据库查询获得）
            obj_in: 更新数据，可以是 Pydantic Schema 或字典

        Returns:
            更新后的 ORM 模型对象
        """
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, obj_id: Any) -> ModelType | None:
        """
        根据主键 ID 删除记录（硬删除）。

        流程：
            1. 先查询记录是否存在
            2. 存在则执行删除并 flush
            3. 不存在则直接返回 None

        Args:
            db: 异步数据库会话
            obj_id: 主键值（支持 int、UUID 等任意类型）

        Returns:
            被删除的 ORM 模型对象，不存在则返回 None
        """
        obj = await self.get(db, obj_id)
        if obj:
            await db.delete(obj)
            await db.flush()
        return obj
