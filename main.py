from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from routers import system

app = FastAPI()

# 全局日志配置
logging.basicConfig(
    level=logging.INFO,  # ⭐ 让 logger.info 生效
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# 打开 SQL 日志（你现在需要）
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

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

app.include_router(system.router)
