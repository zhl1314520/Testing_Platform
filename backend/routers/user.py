from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from core.security import get_current_user
from schemas.user import UserCreate, UserLogin, LoginResponse, UserResponse, UserPageResponse, UserUpdate, ChangePassword
from services import user as user_service
from services.password_reset import send_reset_code, verify_reset_code, reset_password
from DAO import user as user_dao

router = APIRouter(
    prefix="/auth",
    tags=["用户认证"])

"""
GET：获取资源。相当于"给我看看这个用户的信息"。
POST：创建新资源。相当于"帮我创建一个新用户"。
PUT / PATCH：更新资源。相当于"修改一下这个用户的电话号码"。
DELETE：删除资源。相当于"把这个用户删掉"。

    登录：
        服务器上创建了一个新的"会话"（Session）或"令牌"（Token）资源。故使用 post 
"""
@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    return await user_service.login_user(login_data.email, login_data.password, db)


# 获取当前用户信息
"""
显示组件：
- 用户头像和用户名
- 下拉菜单用户信息
"""
@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user = await user_dao.get_user_by_id(current_user["user_id"], db)
    return user


user_router = APIRouter(
    prefix="/users",
    tags=["用户管理"]
)


@user_router.post("", response_model=UserResponse)
async def create_user(
    user_info: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await user_service.create_user(user_info, db)


@user_router.get("", response_model=UserPageResponse)
async def get_user_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await user_service.get_user_list(page, page_size, db)


@user_router.delete("/{id}")
async def delete_user(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    return await user_service.delete_user(id, db)


# 更新用户信息（只允许更新 email 和 role）
@user_router.put("/{id}", response_model=UserResponse)
async def update_user_info(
    id: int,
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 验证是否是用户本人操作
    if current_user["user_id"] != id:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="FORBIDDEN")
    
    return await user_service.update_user(id, user_data, db)


# 修改密码
@user_router.put("/{id}/password")
async def change_user_password(
    id: int,
    password_data: ChangePassword,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user["user_id"] != id:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="FORBIDDEN")
    
    return await user_service.change_password(id, password_data.old_password, password_data.new_password, db)


# 获取用户详细信息
@user_router.get("/{id}", response_model=UserResponse)
async def get_user_detail(
    id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await user_service.get_user_by_id(id, db)


# 密码重置相关路由
password_reset_router = APIRouter(
    prefix="/password-reset",
    tags=["忘记密码"]
)

# 发送验证码
@password_reset_router.post("/send-code")
async def send_code(
    email: str,
    db: AsyncSession = Depends(get_db)
):
    """
    发送密码重置验证码
    """
    return await send_reset_code(email, db)


@password_reset_router.post("/verify-code")
async def verify_code(
    email: str,
    code: str
):
    """
    验证密码重置验证码
    """
    return await verify_reset_code(email, code)


@password_reset_router.post("/reset-password")
async def reset_password(
    email: str,
    code: str,
    new_password: str,
    db: AsyncSession = Depends(get_db)
):
    """
    重置密码
    """
    return await reset_password(email, code, new_password, db)
