
# TMP - 测试管理平台

> **质量至上**

一套全栈测试管理系统，用于管理项目、测试用例、测试执行、缺陷和质量报告。

---

## 技术栈

| 层级 | 技术 |
|------|------|
| **后端** | [FastAPI](https://fastapi.tiangolo.com/) 0.115、[SQLAlchemy](https://www.sqlalchemy.org/) 2.0 (async)、aiomysql、Pydantic 2.9 |
| **前端** | [Vue 3](https://vuejs.org/) 3.4、[Vite](https://vitejs.dev/) 5、Vue Router 4、Axios 1.14、Chart.js 4.5 |
| **数据库** | MySQL 8.0 |
| **认证** | JWT (python-jose)、bcrypt (passlib) |
| **邮件** | aiosmtplib（邮箱验证码重置密码） |

---

## 项目结构

```
TestingMagPlm/
├── backend/                  # FastAPI 后端
│   ├── main.py               # 应用入口
│   ├── requirements.txt      # Python 依赖
│   ├── core/                 # 核心工具
│   │   ├── db.py             # 异步数据库引擎与会话工厂
│   │   └── security.py       # JWT、bcrypt 密码哈希、认证依赖
│   ├── models/               # SQLAlchemy ORM 数据模型
│   │   ├── base.py           # 声明式基类
│   │   ├── user.py           # 用户（PM / 开发 / 测试）
│   │   ├── project.py        # 项目
│   │   ├── project_member.py # 项目成员
│   │   ├── testcase.py       # 测试用例
│   │   ├── execution.py      # 测试执行
│   │   ├── bug.py            # 缺陷
│   │   └── report.py         # 测试报告
│   ├── schemas/              # Pydantic 请求/响应模式
│   ├── routers/              # FastAPI 路由
│   │   ├── user.py           # 认证、用户 CRUD、密码重置
│   │   ├── project.py        # 项目 CRUD、成员管理
│   │   ├── testcase.py       # 用例 CRUD
│   │   ├── execution.py      # 执行 CRUD
│   │   ├── bug.py            # 缺陷 CRUD、状态追踪
│   │   └── report.py         # 报告、统计数据与仪表盘
│   ├── services/             # 业务逻辑层
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── testcase.py
│   │   ├── execution.py
│   │   ├── bug.py
│   │   ├── report.py
│   │   ├── email.py          # 邮件发送
│   │   └── password_reset.py # 验证码重置密码流程
│   └── DAO/                  # 数据访问层（CRUD 操作）
│       ├── user.py
│       ├── project_member.py
│       ├── testcase.py
│       ├── execution.py
│       ├── bug.py
│       ├── report.py
│       └── system.py
├── frontend/                 # Vue 3 前端
│   ├── package.json          # Node.js 依赖
│   ├── vite.config.js        # Vite 配置
│   └── src/
│       ├── main.js           # 应用入口
│       ├── App.vue           # 根组件
│       ├── api/
│       │   └── index.js      # Axios 客户端、拦截器、API 模块
│       ├── router/
│       │   └── index.js      # Vue Router 路由配置与登录守卫
│       ├── styles/
│       │   └── design-system.css  # CSS 变量、渐变色、工具类
│       ├── Login/            # 登录与密码重置页面
│       │   ├── LoginPage.vue
│       │   ├── ForgotPassword.vue
│       │   ├── ResetPassword.vue
│       │   ├── ResetPasswordSuccess.vue
│       │   ├── AnimatedCharacters.vue
│       │   ├── EyeBall.vue
│       │   └── Pupil.vue
│       └── Dashboard/        # 仪表盘页面
│           ├── DashboardLayout.vue  # 布局与导航栏、弹窗、通知
│           ├── Overview.vue          # 概览与图表
│           ├── Projects.vue          # 项目管理
│           ├── TestCases.vue         # 测试用例管理
│           ├── Executions.vue        # 测试执行管理
│           ├── Bugs.vue              # 缺陷追踪
│           └── Reports.vue           # 测试报告
└── tmp_db.sql                # MySQL 数据库建表语句与初始数据
```

---

## 数据库表结构

系统在 `tmp_db` 数据库中使用 7 张核心表：

| 表名 | 描述 | 关键字段 |
|------|------|----------|
| `users` | 系统用户 | username、password（bcrypt）、role、email |
| `projects` | 测试项目 | name、description、owner_id、软删除 |
| `project_members` | 项目成员关系 | project_id、user_id、role |
| `test_cases` | 测试用例 | module、title、steps、expected、status、priority（p0-p3） |
| `executions` | 测试执行记录 | type（手动/自动）、status、pass_rate |
| `bugs` | 缺陷报告 | title、description、status、priority、assignee、reporter |
| `reports` | 测试报告 | pass_rate、fail_rate、total/passed/failed cases |

完整建表语句（含索引、外键和示例数据）参见 `tmp_db.sql`。

---

## API 接口

### 认证与用户管理

| 方法 | 接口 | 说明 |
|------|------|------|
| POST | `/auth/login` | 用户登录，返回 JWT 令牌 |
| GET | `/auth/me` | 获取当前用户信息 |
| POST | `/users` | 创建用户 |
| GET | `/users` | 用户列表（分页） |
| GET | `/users/{id}` | 用户详情 |
| PUT | `/users/{id}` | 更新用户信息（邮箱、角色） |
| DELETE | `/users/{id}` | 删除用户 |
| PUT | `/users/{id}/password` | 修改密码 |

### 密码重置

| 方法 | 接口 | 说明 |
|------|------|------|
| POST | `/password-reset/send-code` | 发送 6 位验证码到邮箱 |
| POST | `/password-reset/verify-code` | 验证验证码 |
| POST | `/password-reset/reset-password` | 使用验证码重置密码 |

### 项目管理

| 方法 | 接口 | 说明 |
|------|------|------|
| POST | `/projects` | 创建项目 |
| GET | `/projects` | 项目列表（分页） |
| PUT | `/projects/{id}` | 更新项目 |
| DELETE | `/projects/{id}` | 删除项目（软删除） |
| POST | `/projects/{id}/members` | 添加项目成员 |
| GET | `/projects/{id}/members` | 查看项目成员 |
| DELETE | `/projects/members/{member_id}` | 移除项目成员 |

### 测试用例管理

| 方法 | 接口 | 说明 |
|------|------|------|
| POST | `/testcases` | 创建测试用例 |
| GET | `/testcases` | 用例列表（分页、可筛选） |
| GET | `/testcases/{id}` | 用例详情 |
| PUT | `/testcases/{id}` | 更新用例 |
| DELETE | `/testcases/{id}` | 删除用例（软删除） |

### 测试执行管理

| 方法 | 接口 | 说明 |
|------|------|------|
| POST | `/executions` | 创建执行记录 |
| GET | `/executions` | 执行列表（分页） |
| GET | `/executions/{id}` | 执行详情 |
| PUT | `/executions/{id}` | 更新执行记录 |
| DELETE | `/executions/{id}` | 删除执行记录 |

### 缺陷管理

| 方法 | 接口 | 说明 |
|------|------|------|
| POST | `/bugs` | 创建缺陷报告 |
| GET | `/bugs` | 缺陷列表（分页、可筛选） |
| GET | `/bugs/{id}` | 缺陷详情 |
| PUT | `/bugs/{id}` | 更新缺陷信息 |
| PUT | `/bugs/{id}/status` | 更新缺陷状态 |
| DELETE | `/bugs/{id}` | 删除缺陷 |

### 报告与数据统计

| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/reports` | 报告列表（分页） |
| DELETE | `/reports/all` | 删除所有报告 |
| GET | `/metrics/overview` | 仪表盘概览统计 |
| GET | `/metrics/trend` | 趋势图表数据 |
| GET | `/metrics/project-progress` | 项目进度数据 |
| GET | `/metrics/recent-activities` | 最近活动列表 |

---

## 快速开始

### 前置要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0

### 后端部署

```bash
cd backend

# 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate    # Linux/Mac

# 安装依赖
pip install -r requirements.txt

# 在 core/db.py 中配置数据库连接
# 默认: mysql+aiomysql://root:123456@localhost:3306/tmp_db

# 初始化数据库
mysql -u root -p < ../tmp_db.sql

# 启动服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API 服务地址: `http://localhost:8000`
API 文档 (FastAPI 自动生成): `http://localhost:8000/docs`

### 前端部署

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

应用地址: `http://localhost:5173`

### 数据库部署

将建表文件导入 MySQL 实例：

```bash
mysql -u root -p
CREATE DATABASE tmp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE tmp_db;
SOURCE tmp_db.sql;
```

或一条命令完成：

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS tmp_db CHARACTER SET utf8mb4;"
mysql -u root -p tmp_db < tmp_db.sql
```

数据库包含示例数据：4 个用户、29 个项目、3 条测试用例、3 条执行记录、3 个缺陷和 3 份报告。

### 默认测试用户

| 用户名 | 角色 | 邮箱 |
|--------|------|------|
| Eric | 开发工程师 | eric@163.com |
| Taylor | 项目经理 | taylor@163.com |
| Charlie | 测试工程师 | 17201665342@163.com |
| testuser | 测试工程师 | test@test.com |

---

## 架构亮点

### 后端

- **全异步架构**：所有数据库操作均使用 `AsyncSession` + `aiomysql` 异步执行
- **三层架构**：路由层（HTTP） → 服务层（业务逻辑） → DAO 层（数据访问）
- **JWT 认证**：基于 Token 的 Bearer 认证，有效期 700 天
- **密码安全**：使用 passlib + bcrypt 进行密码哈希
- **密码重置**：基于邮箱的 6 位验证码机制，60 秒冷却、最多 3 次发送、1 分钟过期
- **软删除**：用户、项目和测试用例均支持软删除
- **CORS**：开发环境下允许所有来源跨域访问

### 前端

- **SPA 路由**：客户端路由 + 登录守卫，未登录自动跳转 `/login`
- **请求拦截器**：自动注入 JWT 令牌到 `Authorization` 请求头；401 响应自动跳转登录页
- **令牌持久化**：令牌持久化存储于浏览器 `localStorage` / `sessionStorage`
- **仪表盘布局**：固定导航栏、用户头像下拉菜单、个人资料弹窗、密码修改弹窗和 Toast 通知
- **设计系统**：基于 CSS 自定义属性的设计系统，橙红主色 / 青绿辅色 / 珊瑚红强调色三色体系，毛玻璃面板，自定义缓动曲线的流畅动效
- **响应式适配**：通过媒体查询适配平板（1024px）和移动端（768px）断点

</div>

<!-- ==================== English Version ==================== -->
<div id="lang-en" class="lang-content">

# TMP - Test Management Platform

> **Quality First**

A full-stack test management system for managing projects, test cases, test executions, bugs, and quality reports.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) 0.115, [SQLAlchemy](https://www.sqlalchemy.org/) 2.0 (async), aiomysql, Pydantic 2.9 |
| **Frontend** | [Vue 3](https://vuejs.org/) 3.4, [Vite](https://vitejs.dev/) 5, Vue Router 4, Axios 1.14, Chart.js 4.5 |
| **Database** | MySQL 8.0 |
| **Auth** | JWT (python-jose), bcrypt (passlib) |
| **Email** | aiosmtplib (password reset via email verification code) |

---

## Project Structure

```
TestingMagPlm/
├── backend/                  # FastAPI backend
│   ├── main.py               # Application entry point
│   ├── requirements.txt      # Python dependencies
│   ├── core/                 # Core utilities
│   │   ├── db.py             # Async DB engine & session factory
│   │   └── security.py       # JWT, bcrypt password hashing, auth dependency
│   ├── models/               # SQLAlchemy ORM models
│   │   ├── base.py           # Declarative base
│   │   ├── user.py           # Users (PM / developer / tester)
│   │   ├── project.py        # Projects
│   │   ├── project_member.py # Project membership
│   │   ├── testcase.py       # Test cases
│   │   ├── execution.py      # Test executions
│   │   ├── bug.py            # Bugs / defects
│   │   └── report.py         # Test reports
│   ├── schemas/              # Pydantic request/response schemas
│   ├── routers/              # FastAPI API routers
│   │   ├── user.py           # Auth, user CRUD, password reset
│   │   ├── project.py        # Project CRUD, member management
│   │   ├── testcase.py       # Test case CRUD
│   │   ├── execution.py      # Test execution CRUD
│   │   ├── bug.py            # Bug CRUD, status tracking
│   │   └── report.py         # Reports, metrics & dashboard data
│   ├── services/             # Business logic layer
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── testcase.py
│   │   ├── execution.py
│   │   ├── bug.py
│   │   ├── report.py
│   │   ├── email.py          # Email sending helper
│   │   └── password_reset.py # Verification code flow for password reset
│   └── DAO/                  # Data Access Objects (CRUD operations)
│       ├── user.py
│       ├── project_member.py
│       ├── testcase.py
│       ├── execution.py
│       ├── bug.py
│       ├── report.py
│       └── system.py
├── frontend/                 # Vue 3 frontend
│   ├── package.json          # Node.js dependencies
│   ├── vite.config.js        # Vite configuration
│   └── src/
│       ├── main.js           # App entry point
│       ├── App.vue           # Root component
│       ├── api/
│       │   └── index.js      # Axios client, interceptors, API modules
│       ├── router/
│       │   └── index.js      # Vue Router config with auth guard
│       ├── styles/
│       │   └── design-system.css  # CSS variables, gradients, utility classes
│       ├── Login/            # Login & password reset pages
│       │   ├── LoginPage.vue
│       │   ├── ForgotPassword.vue
│       │   ├── ResetPassword.vue
│       │   ├── ResetPasswordSuccess.vue
│       │   ├── AnimatedCharacters.vue
│       │   ├── EyeBall.vue
│       │   └── Pupil.vue
│       └── Dashboard/        # Dashboard pages
│           ├── DashboardLayout.vue  # Layout with navbar, modals, toast
│           ├── Overview.vue          # Dashboard overview with charts
│           ├── Projects.vue          # Project management
│           ├── TestCases.vue         # Test case management
│           ├── Executions.vue        # Test execution management
│           ├── Bugs.vue              # Bug / defect tracking
│           └── Reports.vue           # Test reports view
└── tmp_db.sql                # MySQL database schema & seed data
```

---

## Database Schema

The system uses 7 core tables in the `tmp_db` database:

| Table | Description | Key Fields |
|-------|-------------|------------|
| `users` | System users (PM / developer / tester) | username, password (bcrypt), role, email |
| `projects` | Test projects | name, description, owner_id, soft delete |
| `project_members` | Project membership | project_id, user_id, role |
| `test_cases` | Test case definitions | module, title, steps, expected, status, priority (p0-p3) |
| `executions` | Test execution records | type (manual/auto), status, pass_rate |
| `bugs` | Bug / defect reports | title, description, status, priority, assignee, reporter |
| `reports` | Test execution reports | pass_rate, fail_rate, total/passed/failed cases |

See `tmp_db.sql` for the full schema with indexes, foreign keys, and sample data.

---

## API Endpoints

### Authentication & Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | User login, returns JWT token |
| GET | `/auth/me` | Get current user info |
| POST | `/users` | Create a new user |
| GET | `/users` | List users (paginated) |
| GET | `/users/{id}` | Get user detail |
| PUT | `/users/{id}` | Update user (email, role) |
| DELETE | `/users/{id}` | Delete user |
| PUT | `/users/{id}/password` | Change password |

### Password Reset

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/password-reset/send-code` | Send 6-digit verification code to email |
| POST | `/password-reset/verify-code` | Verify the code |
| POST | `/password-reset/reset-password` | Reset password with verified code |

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/projects` | Create a project |
| GET | `/projects` | List projects (paginated) |
| PUT | `/projects/{id}` | Update project |
| DELETE | `/projects/{id}` | Delete project (soft) |
| POST | `/projects/{id}/members` | Add member to project |
| GET | `/projects/{id}/members` | List project members |
| DELETE | `/projects/members/{member_id}` | Remove member |

### Test Cases

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/testcases` | Create test case |
| GET | `/testcases` | List cases (paginated, filterable) |
| GET | `/testcases/{id}` | Get case detail |
| PUT | `/testcases/{id}` | Update case |
| DELETE | `/testcases/{id}` | Delete case (soft) |

### Test Executions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/executions` | Create execution record |
| GET | `/executions` | List executions (paginated) |
| GET | `/executions/{id}` | Get execution detail |
| PUT | `/executions/{id}` | Update execution |
| DELETE | `/executions/{id}` | Delete execution |

### Bugs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/bugs` | Create bug report |
| GET | `/bugs` | List bugs (paginated, filterable) |
| GET | `/bugs/{id}` | Get bug detail |
| PUT | `/bugs/{id}` | Update bug |
| PUT | `/bugs/{id}/status` | Update bug status |
| DELETE | `/bugs/{id}` | Delete bug |

### Reports & Metrics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reports` | List reports (paginated) |
| DELETE | `/reports/all` | Delete all reports |
| GET | `/metrics/overview` | Dashboard overview stats |
| GET | `/metrics/trend` | Trend data for charts |
| GET | `/metrics/project-progress` | Project progress data |
| GET | `/metrics/recent-activities` | Recent activity feed |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL 8.0

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate    # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure database connection in core/db.py
# Default: mysql+aiomysql://root:123456@localhost:3306/tmp_db

# Initialize database (import the SQL schema)
mysql -u root -p < ../tmp_db.sql

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.
API docs (auto-generated by FastAPI): `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

The app will be available at `http://localhost:5173`.

### Database Setup

Import the schema file into your MySQL instance:

```bash
mysql -u root -p
CREATE DATABASE tmp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE tmp_db;
SOURCE tmp_db.sql;
```

Or with a single command:

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS tmp_db CHARACTER SET utf8mb4;"
mysql -u root -p tmp_db < tmp_db.sql
```

The database includes sample data: 4 users, 29 projects, 3 test cases, 3 executions, 3 bugs, and 3 reports.

### Default Users

| Username | Role | Email |
|----------|------|-------|
| Eric | developer | eric@163.com |
| Taylor | PM | taylor@163.com |
| Charlie | tester | 17201665342@163.com |
| testuser | tester | test@test.com |

---

## Architecture Highlights

### Backend

- **Async-first**: All database operations use `AsyncSession` with `aiomysql`
- **Three-layer architecture**: Routers (HTTP) → Services (business logic) → DAO (data access)
- **JWT authentication**: Token-based auth with HTTP Bearer scheme, 700-day expiry
- **Password security**: bcrypt hashing via passlib
- **Password reset**: Email-based 6-digit verification code flow with rate limiting (60s cooldown, max 3 attempts) and 1-minute expiry
- **Soft deletes**: `deleted_at` column on users, projects, and test cases
- **CORS**: Enabled for all origins (development)

### Frontend

- **SPA with Vue Router**: Client-side routing with auth guard (redirects to `/login` if no token)
- **Axios interceptors**: Automatic JWT token injection into `Authorization` header; 401 response redirects to login
- **Token persistence**: Stored in `localStorage` / `sessionStorage`
- **Dashboard layout**: Fixed navbar with navigation, user avatar dropdown, profile modal, password change modal, and toast notifications
- **Design system**: CSS custom properties-based design system with ember/orange primary, teal secondary, coral accent color palette; glassmorphism panels; smooth animations with custom easing curves
- **Responsive**: Media queries for tablet (1024px) and mobile (768px) breakpoints

</div>

<script>
function switchLang(lang) {
  document.querySelectorAll('.lang-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.lang-btn').forEach(el => el.classList.remove('active'));
  document.getElementById('lang-' + lang).classList.add('active');
  event.target.classList.add('active');
}
</script>

</body>
</html>
