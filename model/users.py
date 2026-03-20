from sqlalchemy import Integer, String, Enum, DateTime, Index, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

# 父类只做字段定义，不建表
class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="ID")
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="邮箱")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码（加密存储）")
    avatar: Mapped[str] = mapped_column(String(255), default='', comment="头像URL")
    gender: Mapped[str] = mapped_column(Enum('male', 'female', name='gender_enum'), comment="性别")
    position: Mapped[str] = mapped_column(String(100), comment="职位")
    phone: Mapped[str] = mapped_column(String(20), unique=True, comment="手机号")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),
                                                 onupdate=func.now(), comment="更新时间")
    # 用这3个字段原因：快速识别对象身份。（用别的也行，只是没有这些好些）
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', phone='{self.phone}')>"

# Admin 表
class Admin(User):
    __tablename__ = "admin_user"
    # 这个子类使用具体表继承
    __mapper_args__ = {'concrete': True}
    # 索引
    __table_args__ = (
        Index('admin_email_UNIQUE', 'email'),
        Index('admin_phone_UNIQUE', 'phone'),
    )

# Developer 表
class Developer(User):
    __tablename__ = "developer_user"
    __mapper_args__ = {'concrete': True}
    __table_args__ = (
        Index('dev_email_UNIQUE', 'email'),
        Index('dev_phone_UNIQUE', 'phone'),
    )

# Tester 表
class Tester(User):
    __tablename__ = "tester_user"
    __mapper_args__ = {'concrete': True}
    __table_args__ = (
        Index('tester_email_UNIQUE', 'email'),
        Index('tester_phone_UNIQUE', 'phone'),
    )



class AdminToken(Base):
    __tablename__ = "admin_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("admin_user.id"), nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __repr__(self):
        return f"<AdminToken(id={self.id}, user_id={self.user_id}, token='{self.token[:8]}...')>"


class DeveloperToken(Base):
    __tablename__ = "developer_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("developer_user.id"), nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)        # 不用建立索引，这行相当于建立了索引
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __repr__(self):
        return f"<DeveloperToken(id={self.id}, user_id={self.user_id}, token='{self.token[:8]}...')>"


class TesterToken(Base):
    __tablename__ = "tester_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("tester_user.id"), nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __repr__(self):
        return f"<TesterToken(id={self.id}, user_id={self.user_id}, token='{self.token[:8]}...')>"