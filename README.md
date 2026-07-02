# FastAPI Starter

FastAPI 项目模板

## 项目结构

### 本地开发

```bash
# 1. 创建虚拟环境
# 作用：在当前目录下创建一个名为 .venv 的独立 Python 虚拟环境，用于隔离项目依赖，避免污染全局 Python 环境。
python -m venv .venv

# 2. 激活虚拟环境
# 作用：激活刚刚创建的虚拟环境。激活成功后，终端命令行提示符最左侧会出现 (.venv) 标识。
# 注意：以下命令适用于 macOS / Linux 系统。
source .venv/bin/activate
# 补充：如果你使用的是 Windows (CMD/PowerShell)，请使用以下命令激活：
# .venv\Scripts\activate

# 3. 安装依赖
# 作用：安装 FastAPI 框架及其标准依赖包（包含 uvicorn 服务器、fastapi-cli 等开发必备工具）。
pip install "fastapi[standard]"

# 4. 启动服务
# 作用：启动 FastAPI 本地开发服务器，并开启代码热重载（修改代码后自动重启）。
fastapi dev

# 或者使用传统的 uvicorn 启动方式：
# uvicorn app.main:app --reload --port 8000

# 5. 退出虚拟环境
# 作用：开发或调试完成后，退出当前的虚拟环境，使终端恢复到系统的全局 Python 环境。
deactivate
```

### 使用 uv 管理项目

```bash
# 1. 安装 uv
pip install uv

# 2. 在当前目录初始化项目（会自动生成 pyproject.toml、.python-version 等）
uv init

# 3. 进入目录并添加依赖（它会自动更新 pyproject.toml 和生成 uv.lock）
uv add "fastapi[standard]"

# 4. 同步环境
uv sync

# 5. 直接运行，uv 会自动处理环境
uv run fastapi dev
```

### 安装开发依赖

Ruff：集 Linter 和 Formatter 于一身。替代了 Black, isort, flake8 及其数十个插件。
Mypy 或 Pyright：静态类型检查器。“没有类型提示的代码等于没有写完的代码” 已成为行业共识。

```bash
# --dev 参数将这些包标记为开发依赖（写入 [dependency-groups].dev）
uv add --dev ruff mypy

# 检查代码风格并自动修复（包括 import 排序、移除未使用的导入等）
uv run ruff check --fix .

# 格式化所有 Python 文件（统一引号风格、缩进、行宽等）
uv run ruff format .

# CI 环境中的只读检查（不修改文件，发现问题则退出码非 0）：
# uv run ruff check .
# uv run ruff format --check .

# 运行静态类型检查（项目需配置 pyproject.toml 中的 [tool.mypy]）
uv run mypy app/

# 首次运行建议加 --strict 发现所有潜在问题
# uv run mypy --strict app/
```

### Git 钩子自动检查

Pre-commit：Git 钩子管理框架，确保代码在提交前必须通过格式化和检查。

```bash
uv add --dev pre-commit

# 安装钩子（只需执行一次）：
uv run pre-commit install

# 手动运行验证

# 对所有已跟踪的文件运行所有钩子（首次设置时推荐）
uv run pre-commit run --all-files

# 仅对暂存区的文件运行（模拟 git commit 时的行为）
uv run pre-commit run

# 清理旧缓存
uv run pre-commit clean
```
