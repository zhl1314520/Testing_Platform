from typing import List

from pydantic import BaseModel, Field

# 返回给前端的数据结构
class SystemResponse(BaseModel):
    id: int
    name: str
    description: str | None

    class Config:
        from_attributes = True  # 支持 ORM 对象转换

# 创建系统请求参数
class SystemCreate(BaseModel):
    name: str = Field(..., max_length=100)  # 限制长度
    description: str | None = None


# 分页请求参数
class PageParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
# 分页返回结构
class SystemPageResponse(BaseModel):
    total: int
    items: List[SystemResponse]     # 返回 SystemResponse 里面有的参数。