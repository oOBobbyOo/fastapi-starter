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
