from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db
from schemas.system import SystemCreate, SystemResponse
from services import system as service

router = APIRouter(
    prefix="/system",
    tags=["项目系统管理"]
)

# 创建系统接口
@router.post(
    "/create",
    response_model=SystemResponse,
    status_code=201  # 创建资源
)
async def create_system(
    system_info: SystemCreate,
    db: AsyncSession = Depends(get_db)
):
    return await service.create_system(system_info, db)

# @router.get("/get_system_list")
# async def get_system_list(
#         page: int = Query(1, ge=1),
#         page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
#         user: User = Depends(get_current_user),
#         db: AsyncSession = Depends(get_db)
# )
