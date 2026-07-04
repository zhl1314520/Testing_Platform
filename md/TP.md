```sql
CREATE TABLE system_name (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name varchar(100) NOT NULL,
  description varchar(255) DEFAULT NULL,
  created_at datetime DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);



CREATE TABLE api (
    id INT AUTO_INCREMENT PRIMARY KEY,
    system_id INT NOT NULL,
    name VARCHAR(100),
    url VARCHAR(255),
    method VARCHAR(10),
    headers JSON,
    body JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_project_id (project_id)
);


CREATE TABLE testcase (
    id INT AUTO_INCREMENT PRIMARY KEY,
    api_id INT NOT NULL,
    name VARCHAR(100),
    expected_status INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_api_id (api_id)
);



CREATE TABLE testcase_assertion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_id INT NOT NULL,
    type VARCHAR(50),          -- 断言类型（status_code/json）
    expression VARCHAR(255),  -- JSONPath
    expected_value VARCHAR(255),
    INDEX idx_case_id (case_id)
);




CREATE TABLE test_run (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_id INT NOT NULL,
    status TINYINT, -- 0失败 1成功
    run_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_case_id (case_id)
);


CREATE TABLE test_run_detail (
    id INT AUTO_INCREMENT PRIMARY KEY,
    run_id INT NOT NULL,
    response_status INT,
    response_body JSON,
    assertion_result TINYINT,
    error_message TEXT,
    INDEX idx_run_id (run_id)
);



文件架构：
project_root/
│
├── app/                        # 主应用目录（核心代码）
│
│   ├── main.py                # 入口文件
│
│   ├── core/                  # 核心配置
│   │   ├── config.py          # 配置（数据库、环境变量）
│   │   ├── db.py              # 数据库连接（你现在的 db_config）
│   │
│   ├── models/                # ORM模型
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── system.py
│   │
│   ├── schemas/               # Pydantic（入参/出参）
│   │   ├── __init__.py
│   │   ├── system.py
│   │
│   ├── crud/                  # 数据库操作层（纯SQL操作）
│   │   ├── __init__.py
│   │   ├── system.py
│   │
│   ├── services/              # 业务逻辑层（核心）
│   │   ├── __init__.py
│   │   ├── system.py
│   │
│   ├── api/                   # 路由层
│   │   ├── __init__.py
│   │   ├── deps.py            # 依赖（get_db等）
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── router.py      # 总路由
│   │       ├── system.py      # system接口
│
│   ├── utils/                 # 工具类
│   │   ├── __init__.py
│   │   ├── response.py        # 统一返回格式
│   │
│   ├── exceptions/            # 自定义异常
│   │   ├── __init__.py
│   │   ├── custom.py
│
│
├── tests/                     # 测试
│   ├── test_system.py
│
├── requirements.txt
├── README.md
```

```js
用户操作 (点击/输入)
    ↓
Vue 组件处理 (验证、状态管理)
    ↓
调用 API (fetch/axios) → POST /api/login
    ↓
FastAPI 接收请求 → 验证 → 返回 JSON
    ↓
Vue 接收响应 → 更新状态 → 渲染 UI
    ↓
用户看到结果 (跳转/提示错误)
```

# 企业级测试平台功能文档

## 1️⃣ 用户与权限管理

企业级系统必须有清晰的身份管理和权限控制。

### 功能点：

- **用户管理**：员工账号创建、删除、信息管理
- **权限角色**：
  - **管理员**：可以配置平台、管理用户、管理项目
  - **测试工程师**：执行测试、查看报告、提交缺陷
  - **开发工程师**：查看相关测试结果、跟踪缺陷
- **权限细分**：按项目和功能进行精细化权限控制

## 2️⃣ 项目管理模块

- 项目创建、删除、修改
- 测试环境配置（服务器、数据库等）
- 测试类型管理（单元测试、接口测试、性能测试、UI自动化测试）
- 团队成员管理（负责人、测试人员、开发人员）
- 版本管理（Release/Build号绑定）

## 3️⃣ 测试用例管理

- 用例库分类管理（模块/功能/业务线）
- 用例编写规范（输入、输出、前置条件、步骤、期望结果）
- 用例导入/导出（Excel、CSV、JSON）
- 用例状态管理（新建、已执行、失败、通过、阻塞）
- 用例关联缺陷或自动化脚本

## 4️⃣ 测试执行模块

- 执行方式：手动执行、自动执行（CI/CD集成）
- 测试环境选择（服务器、数据库、浏览器、操作系统）
- 执行队列管理（并发、优先级、计划任务）
- 执行日志与实时监控（进度、失败原因、截图/视频）

## 5️⃣ 报告与分析模块

- 测试报告生成（通过率、失败率、覆盖率）
- 趋势分析（用例通过率、Bug新增/关闭趋势）
- 缺陷统计（按模块、严重级别、负责人）
- 报告导出功能（PDF/Excel）

## 6️⃣ 缺陷管理

- 缺陷录入（关联测试用例、项目、版本）
- 缺陷状态管理（新建、处理中、已解决、已关闭、延期）
- 优先级管理（严重、中等、轻微）
- 分配与通知（开发人员、邮件/消息提醒）

## 7️⃣ 自动化集成与执行

- 脚本管理（Python、Java、Selenium、Appium、Postman集合）
- 自动化触发（CI/CD集成、定时任务）
- 测试结果回传（自动标记用例状态、生成可视化报告）

## 8️⃣ 数据与指标统计

- 测试覆盖率统计
- 执行效率统计（平均执行时间、失败率、阻塞率）
- 用例和缺陷分析（高风险模块、稳定性分析）
- 自定义报表生成和邮件发送

## 9️⃣ 系统与运维管理

- 日志管理（操作日志、执行日志、异常日志）
- 告警与通知（执行失败、系统异常）
- 系统配置（测试环境、邮箱、存储、并发线程）
- 备份与恢复（数据库、报告、脚本）

