from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import users

app = FastAPI()


"""
@app.get("/")
async def root():
    return {"message": "Hello World"}
"""
# 挂载/注册 全局异常处理器
# register_exception_handlers(app)

# 配置 CORS 中间件，允许跨域请求（解决前后端跨域问题）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源(开发时可以使用*，生产环境建议指定具体的域名)
    allow_credentials=True,  # 允许携带凭证（如Cookies）
    allow_methods=["*"],  # 允许所有请求方法
    allow_headers=["*"],  # 允许所有请求头
)

app.include_router(users.router)
