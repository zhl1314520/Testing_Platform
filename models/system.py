from sqlalchemy import String, DateTime, func, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from models.base import Base


# 系统表
class System(Base):
    __tablename__ = "system_name"

    __table_args__ = (
        Index("idx_system_name", "name"),
    )

    # 主键ID（自增）
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 系统名称（唯一）
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # 描述
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # 创建时间
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # 更新时间
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )