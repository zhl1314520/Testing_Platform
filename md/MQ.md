## 🎯 RabbitMQ 在项目中的最佳应用场景

### 一、推荐添加消息队列的场景（按优先级排序）

#### 1. 🧪 测试执行任务（**强烈推荐，面试核心亮点**）

**位置**: `services/execution.py` 和 `routers/execution.py`

**业务场景**:
- 测试执行可能是耗时操作（运行测试用例、收集结果）
- 用户点击"运行"后不应该等待，而是异步执行
- 可以展示任务状态、进度

```
┌──────────┐     ┌──────────┐     ┌──────────────┐     ┌──────────┐
│  用户    │────▶│  API     │────▶│  RabbitMQ    │────▶│  Worker  │
│ 点击运行 │     │ 立即返回 │     │  消息队列    │     │ 执行测试 │
└──────────┘     └──────────┘     └──────────────┘     └──────────┘
                      │                                       │
                      ▼                                       ▼
                 ┌──────────┐                          ┌──────────┐
                 │ 返回任务 │                          │ 更新状态 │
                 │   ID     │                          │ 写入结果 │
                 └──────────┘                          └──────────┘
```

**实现示例**:

```python
# backend/core/queue.py
import pika
import json

class TaskQueue:
    def __init__(self, host='localhost'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='test_execution', durable=True)
    
    def publish_task(self, queue_name: str, task_data: dict):
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(task_data),
            properties=pika.BasicProperties(delivery_mode=2)
        )
    
    def consume_task(self, queue_name: str, callback):
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=False
        )
        self.channel.start_consuming()

task_queue = TaskQueue()
```

```python
# backend/services/execution.py
from core.queue import task_queue

async def create_execution_task(execution_id: int, project_id: int, user_id: int):
    task_data = {
        "task_type": "test_execution",
        "execution_id": execution_id,
        "project_id": project_id,
        "user_id": user_id,
        "created_at": datetime.now().isoformat()
    }
    task_queue.publish_task("test_execution", task_data)
    return {"status": "queued", "execution_id": execution_id}
```

```python
# backend/workers/execution_worker.py
import asyncio
from core.queue import task_queue
from DAO.execution import update_execution_status
from core.db import get_db

def process_execution(ch, method, properties, body):
    task = json.loads(body)
    execution_id = task["execution_id"]
    
    # 更新状态为执行中
    asyncio.run(update_execution_status(execution_id, "执行中"))
    
    try:
        # 模拟测试执行
        result = run_tests(task["project_id"])
        
        # 更新状态为完成
        asyncio.run(update_execution_result(execution_id, result))
    except Exception as e:
        asyncio.run(update_execution_status(execution_id, "失败"))
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == "__main__":
    task_queue.consume_task("test_execution", process_execution)
```

**面试亮点**:
> "测试执行是典型的耗时操作。我将执行任务放入 RabbitMQ 队列，由独立的 Worker 异步处理。这样 API 可以立即返回，用户体验更好，同时也实现了执行任务的削峰填谷，避免高并发时服务器压力过大。"

---

#### 2. 📧 异步邮件/通知发送

**位置**: `services/user.py` 中的密码重置、用户注册

**业务场景**:
- 发送邮件是耗时操作（连接 SMTP 服务器）
- 不应该阻塞用户请求
- 失败可以重试

```python
# backend/services/notification.py
from core.queue import task_queue

async def send_password_reset_email(email: str, code: str):
    task_data = {
        "task_type": "send_email",
        "email_type": "password_reset",
        "to": email,
        "code": code
    }
    task_queue.publish_task("notifications", task_data)
```

```python
# backend/workers/notification_worker.py
import smtplib

def send_email(ch, method, properties, body):
    task = json.loads(body)
    
    try:
        # 发送邮件逻辑
        smtp = smtplib.SMTP('smtp.example.com', 587)
        smtp.sendmail(...)
        smtp.quit()
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        # 失败重试或进入死信队列
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
```

---

#### 3. 📊 报表生成

**位置**: `services/report.py`

**业务场景**:
- 复杂报表生成可能耗时较长
- 可以异步生成后通知用户

```python
async def generate_report_task(report_id: int, filters: dict):
    task_data = {
        "task_type": "generate_report",
        "report_id": report_id,
        "filters": filters
    }
    task_queue.publish_task("report_generation", task_data)
    return {"status": "generating", "report_id": report_id}
```

---

#### 4. 📝 操作日志记录

**位置**: 全局中间件或装饰器

**业务场景**:
- 每次请求都记录日志会影响性能
- 异步写入提升响应速度

```python
# backend/middleware/logging.py
from core.queue import task_queue

async def log_request_middleware(request: Request, call_next):
    response = await call_next(request)
    
    log_data = {
        "task_type": "access_log",
        "path": request.url.path,
        "method": request.method,
        "user_id": request.state.user_id,
        "timestamp": datetime.now().isoformat()
    }
    task_queue.publish_task("logs", log_data)
    
    return response
```

---

### 二、推荐的架构设计

```
                        ┌─────────────────────────────────────────┐
                        │              FastAPI 应用                │
                        └─────────────────┬───────────────────────┘
                                          │
              ┌───────────────────────────┼───────────────────────────┐
              │                           │                           │
              ▼                           ▼                           ▼
    ┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
    │  测试执行请求    │        │  邮件发送请求    │        │  报表生成请求    │
    └────────┬────────┘        └────────┬────────┘        └────────┬────────┘
             │                          │                          │
             └──────────────────────────┼──────────────────────────┘
                                        │
                                        ▼
                        ┌───────────────────────────────┐
                        │          RabbitMQ             │
                        │  ┌─────────────────────────┐  │
                        │  │  test_execution Queue   │  │
                        │  ├─────────────────────────┤  │
                        │  │  notifications Queue    │  │
                        │  ├─────────────────────────┤  │
                        │  │  reports Queue          │  │
                        │  ├─────────────────────────┤  │
                        │  │  logs Queue             │  │
                        │  └─────────────────────────┘  │
                        └───────────────┬───────────────┘
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              │                         │                         │
              ▼                         ▼                         ▼
    ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
    │ Execution Worker│      │Notification Wkr│      │  Report Worker  │
    │   (测试执行)     │      │   (邮件通知)    │      │   (报表生成)    │
    └─────────────────┘      └─────────────────┘      └─────────────────┘
```

---

### 三、完整目录结构建议

```
backend/
├── core/
│   ├── db.py
│   ├── security.py
│   ├── cache.py          # Redis 缓存
│   └── queue.py          # RabbitMQ 连接
├── workers/
│   ├── __init__.py
│   ├── execution_worker.py   # 测试执行 Worker
│   ├── notification_worker.py # 通知 Worker
│   └── report_worker.py      # 报表 Worker
├── services/
│   └── task_service.py       # 任务发布服务
└── main.py
```

---

### 四、面试时如何突出（话术建议）

| 问题                     | 回答要点                                                     |
| ------------------------ | ------------------------------------------------------------ |
| **为什么用 RabbitMQ？**  | 解耦、异步、削峰填谷、可靠消息投递                           |
| **为什么不用 Celery？**  | RabbitMQ 更轻量、学习成本低、适合中小项目；Celery 底层也可以用 RabbitMQ |
| **如何保证消息不丢失？** | 消息持久化、消费者手动 ACK、死信队列                         |
| **如何保证消息顺序？**   | 单队列单消费者、或使用消息分组                               |
| **消息积压怎么办？**     | 增加消费者、优化处理逻辑、监控告警                           |
| **如何实现延迟任务？**   | RabbitMQ 延迟插件、或使用 TTL + 死信队列                     |

---

### 五、RabbitMQ + Redis 组合拳（**面试加分**）

```
┌────────────┐     ┌────────────┐     ┌────────────┐
│   用户     │────▶│   API      │────▶│  RabbitMQ  │
└────────────┘     └────────────┘     └─────┬──────┘
                                             │
                                             ▼
                                      ┌────────────┐
                                      │   Worker   │
                                      └─────┬──────┘
                                            │
                         ┌──────────────────┼──────────────────┐
                         ▼                  ▼                  ▼
                  ┌────────────┐     ┌────────────┐     ┌────────────┐
                  │  执行测试  │     │ 更新数据库 │     │ 写入 Redis │
                  └────────────┘     └────────────┘     │ 缓存结果   │
                                                        └────────────┘
```

**面试亮点**:
> "我设计了 Redis + RabbitMQ 的组合架构：Redis 缓存热点数据提升读取性能，RabbitMQ 处理耗时任务实现异步解耦。测试执行时，任务先入队列，Worker 异步处理后更新数据库并刷新缓存，既保证了响应速度，又确保了数据一致性。"

---

### 六、推荐实现顺序

| 优先级 | 功能           | 面试价值                   |
| ------ | -------------- | -------------------------- |
| ⭐⭐⭐    | 测试执行异步化 | 展示异步架构、削峰填谷     |
| ⭐⭐⭐    | 邮件/通知异步  | 展示解耦思想、提升用户体验 |
| ⭐⭐     | 报表生成       | 展示大数据量处理能力       |
| ⭐      | 操作日志       | 展示性能优化意识           |

这样的设计既能提升系统性能和可扩展性，又能在面试中展示你对 **异步架构、消息队列、系统解耦** 的深入理解！