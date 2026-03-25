from pydantic import BaseModel, Field


# 创建系统请求参数
class SystemCreate(BaseModel):
    name: str = Field(..., max_length=100)  # 限制长度
    description: str | None = None


# 返回给前端的数据结构
class SystemResponse(BaseModel):
    id: int
    name: str
    description: str | None

    class Config:
        from_attributes = True  # 支持 ORM 对象转换
