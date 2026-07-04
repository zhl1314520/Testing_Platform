"""
用户模型模块

对应数据库表：users
描述：存储系统用户信息，包括 PM、developer、tester 三种角色
"""
from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class User(Base):
    """
    用户模型类
    
    对应数据库表：users
    
    Attributes:
        id: 用户 ID（主键，自增）
        username: 用户名（唯一，最多 15 字符）
        password: 密码（bcrypt 加密，最多 110 字符）
        role: 角色（PM/developer/tester）
        email: 邮箱（唯一，最多 50 字符）
        created_at: 创建时间（自动填充）
        updated_at: 更新时间（自动更新）
        deleted_at: 软删除时间（可选）
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True, 
        comment="用户 ID"
    )
    username: Mapped[str] = mapped_column(
        String(15), 
        unique=True, 
        nullable=False, 
        comment="用户名"
    )
    password: Mapped[str] = mapped_column(
        String(110), 
        nullable=False, 
        comment="密码（bcrypt 加密）"
    )
    role: Mapped[str] = mapped_column(
        String(20), 
        nullable=False, 
        comment="角色 (PM/developer/tester)"
    )
    email: Mapped[str] = mapped_column(
        String(50), 
        unique=True, 
        nullable=False, 
        comment="邮箱"
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, 
        server_default=func.now(), 
        comment="创建时间"
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, 
        server_default=func.now(), 
        onupdate=func.now(), 
        comment="更新时间"
    )
    deleted_at: Mapped[DateTime] = mapped_column(
        DateTime, 
        nullable=True, 
        comment="软删除时间"
    )

    # Debug
    def __repr__(self):
        return (
            f"<User id={self.id} "
            f"username='{self.username}' "
            f"role='{self.role}' "
            f"email='{self.email}'>")
