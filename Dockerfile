# 使用 Python 3.12 轻量镜像（第三方依赖兼容性更稳）
FROM python:3.12-slim

# 关闭 pyc 生成并确保日志实时输出
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 设置工作目录
WORKDIR /code

# 先复制依赖声明，利用 Docker 层缓存
COPY ./pyproject.toml /code/pyproject.toml

# 安装运行依赖（与 pyproject.toml 保持一致）
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir "fastapi>=0.136.0" "uvicorn>=0.44.0"

# 再复制完整项目代码（包括静态文件）
COPY . /code

# 对外暴露服务端口

# 对外暴露 8000 端口
EXPOSE 8000

# 启动时指定端口为 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]