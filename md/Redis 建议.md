## 🎯 Redis 缓存最佳添加位置分析

### 一、推荐添加缓存的场景（按优先级排序）

#### 1. 📊 统计指标缓存（**强烈推荐，面试亮点**）

**位置**: DAO/report.py 中的 get_metrics_overview 和 get_metrics_trend

**理由**:

- 这些统计数据涉及多表联查、聚合计算，**查询耗时较长**
- 数据不需要实时精确，**允许短时间延迟**
- 访问频率高（每次进入 Overview 页面都会调用）

```
# 建议实现示例
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def get_metrics_overview(db: AsyncSession):
    cache_key = "metrics:overview"
    cached = redis_client.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    # 原有的数据库查询逻辑...
    result = {...}
    
    # 缓存5分钟
    redis_client.setex(cache_key, 300, json.dumps(result))
    return result
```

**面试亮点**:

> "我选择在统计指标模块引入 Redis 缓存，因为这些数据涉及多表聚合查询，QPS 较高但实时性要求不高。通过设置 5 分钟过期时间，有效降低了数据库压力，页面响应时间从 800ms 降到了 50ms。"

------

#### 2. 👤 用户信息缓存

**位置**: DAO/user.py 中的 get_user_by_id 和 get_user_by_email

**理由**:

- 用户信息在每次请求认证时都会查询
- 用户信息变更频率低
- 可以配合 JWT 实现快速鉴权

```
async def get_user_by_id(user_id: int, db: AsyncSession):
    cache_key = f"user:{user_id}"
    cached = redis_client.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if user:
        redis_client.setex(cache_key, 1800, json.dumps({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }))
    
    return user
```

**缓存失效策略**: 用户信息修改时主动删除缓存

------

#### 3. 🔐 Token 黑名单（**面试加分项**）

**位置**: core/security.py 或新建 core/cache.py

**理由**:

- 用户登出时需要立即使 Token 失效
- JWT 本身无法主动失效，需要配合缓存实现
- 展示对 **JWT 安全性** 的深入理解

```
# 登出时添加到黑名单
async def logout(token: str):
    redis_client.setex(f"token:blacklist:{token}", 3600, "1")

# 验证时检查黑名单
async def verify_token(token: str):
    if redis_client.exists(f"token:blacklist:{token}"):
        raise HTTPException(status_code=401, detail="Token已失效")
    # 继续验证...
```

**面试亮点**:

> "JWT 的一个痛点是无法主动失效。我通过 Redis 实现 Token 黑名单机制，用户登出时将 Token 加入黑名单，验证时先检查黑名单，既保留了 JWT 的无状态优势，又解决了安全退出的问题。"

------

#### 4. 📋 项目列表缓存

**位置**: DAO/project.py 中的 get_project_list

**理由**:

- 项目列表是高频访问接口
- 数据变更频率相对较低
- 可以按用户 ID 分组缓存

------

### 二、推荐的缓存架构设计



------

### 三、完整实现建议

#### 创建缓存工具类 backend/core/cache.py

```
import redis
import json
from typing import Optional, Any
from functools import wraps
import asyncio

class RedisCache:
    def __init__(self, host: str = "localhost", port: int = 6379, 
    db: int = 0):
        self.client = redis.Redis(host=host, port=port, db=db, 
        decode_responses=True)
    
    def get(self, key: str) -> Optional[Any]:
        try:
            value = self.client.get(key)
            return json.loads(value) if value else None
        except:
            return None
    
    def set(self, key: str, value: Any, expire: int = 300):
        try:
            self.client.setex(key, expire, json.dumps(value, 
            default=str))
        except:
            pass
    
    def delete(self, key: str):
        try:
            self.client.delete(key)
        except:
            pass
    
    def delete_pattern(self, pattern: str):
        """删除匹配模式的所有缓存"""
        try:
            keys = self.client.keys(pattern)
            if keys:
                self.client.delete(*keys)
        except:
            pass

cache = RedisCache()

def cached(key_prefix: str, expire: int = 300):
    """缓存装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{key_prefix}:{':'.join(map(str, args
            [1:3]))}"
            
            cached_result = cache.get(cache_key)
            if cached_result:
                return cached_result
            
            result = await func(*args, **kwargs)
            
            if result:
                cache.set(cache_key, result, expire)
            
            return result
        return wrapper
    return decorator
```

------

### 四、面试时如何突出（话术建议）

| 问题                 | 回答要点                                                 |
| -------------------- | -------------------------------------------------------- |
| **为什么用 Redis？** | 高性能（内存存储）、丰富数据结构、支持持久化、原子操作   |
| **缓存策略是什么？** | Cache-Aside 模式，读时先查缓存，写时先更新数据库再删缓存 |
| **如何保证一致性？** | 延迟双删、设置合理过期时间、关键数据使用分布式锁         |
| **缓存穿透怎么办？** | 布隆过滤器、空值缓存                                     |
| **缓存击穿怎么办？** | 互斥锁、热点数据永不过期                                 |
| **缓存雪崩怎么办？** | 过期时间加随机值、多级缓存、熔断降级                     |

------

### 五、推荐优先实现的顺序

1. **统计指标缓存** - 效果最明显，面试最容易讲清楚
2. **Token 黑名单** - 展示对 JWT 安全的深入理解
3. **用户信息缓存** - 基础且实用
4. **项目列表缓存** - 补充完善