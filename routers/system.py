from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from schemas.system import SystemCreate, SystemResponse, SystemPageResponse
from services import system as service

router = APIRouter(
    prefix="/system",
    tags=["项目系统管理"]
)

# 创建系统接口
"""
    response_model=SystemPageResponse 告诉 FastAPI 返回的数据结构
    将 SQLAlchemy ORM 对象自动转化为 dict / json 发前端
"""
@router.post(
    "/create",
    response_model=SystemResponse
)
async def create_system(
    system_info: SystemCreate,
    db: AsyncSession = Depends(get_db)
):
    return await service.create_system(system_info, db)

# 分页查询接口（获取列表
@router.get("/list", response_model=SystemPageResponse)
async def get_system_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_system_list(page, page_size, db)

# 删除系统
@router.delete("/delete/{id}")
async def delete_system(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_system(id, db)
