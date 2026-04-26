from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field

app = FastAPI(
    docs_url=None,  # 关闭 Swagger UI
    redoc_url=None,  # 关闭 ReDoc
    openapi_url=None,  # 关闭 OpenAPI JSON
    title="示例 API",
    description="FastAPI 原生响应格式示例服务。",
    version="0.1.0",
    openapi_tags=[
        {"name": "基础", "description": "健康检查与示例接口。"},
        {"name": "图书", "description": "书籍与作者相关查询。"},
        {"name": "演示", "description": "错误与响应格式演示（仅开发环境使用）。"},
    ],
)


@app.get(
    "/",
    summary="根路径",
    description="返回欢迎信息,用于确认服务可用。",
    tags=["基础"],
    response_description="成功时返回包含 message 字段的字典。",
)
async def root():
    return {"message": "Hello World1233"}


@app.get(
    "/demo/error",
    summary="演示业务错误响应",
    description="故意抛出 HTTP 异常,展示 FastAPI 默认错误响应格式。",
    tags=["演示"],
    response_description="返回 404 状态码及错误详情。",
)
async def demo_error():
    raise HTTPException(status_code=404, detail="示例业务错误")


@app.get(
    "/hello/{name}",
    summary="按姓名问候",
    description="根据路径中的姓名返回问候语。",
    tags=["基础"],
    response_description="成功时返回包含 message 字段的字典。",
)
async def say_hello(
    name: Annotated[str, Path(description="要问候的对方姓名")],
):
    return {"message": f"Hello {name}"}


@app.get(
    "/books/{book_id}",
    summary="按编号查询书籍",
    description="通过路径中的书籍编号查询;编号必须为 1~100 之间的整数。",
    tags=["图书"],
    response_description="成功时返回包含 book_id 及占位字段的字典。",
)
async def get_book(
    book_id: Annotated[
        int,
        Path(
            ge=1,
            le=100,
            description="书籍编号,取值范围 1~100(含边界)",
        ),
    ],
):
    return {"book_id": book_id, "title": None, "note": "示例:此处可接数据库查询"}


@app.get(
    "/authors/{author}",
    summary="按作者查询",
    description="通过路径中的作者名称查询;名称长度须为 2~10 个字符。",
    tags=["图书"],
    response_description="成功时返回包含 author 字段的字典。",
)
async def get_by_author(
    author: Annotated[
        str,
        Path(
            min_length=2,
            max_length=10,
            description="作者名称,长度 2~10 个字符(含边界)",
        ),
    ],
):
    return {"author": author, "books": [], "note": "示例:此处可按作者筛选书籍列表"}


@app.get(
    "/news/list",
    summary="获取新闻列表",
    description="分页获取新闻列表,支持指定跳过数量和返回数量。",
    tags=["新闻"],
    response_description="成功时返回包含 news_list 及分页信息的字典。",
)
async def get_news_list(
    skip: Annotated[int, Query(ge=0, description="跳过记录数,默认0")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="返回记录数,默认10")] = 10,
):
    # 模拟数据生成,实际项目中应从数据库查询
    news_list = [{"title": f"新闻{i + 1}"} for i in range(skip, skip + limit)]
    return {"news_list": news_list, "total": 100, "skip": skip, "limit": limit}


# 登录请求体模型
class LoginRequest(BaseModel):
    username: str = Field(
        min_length=1,
        max_length=16,
        description="用户名",
        examples=["admin"],
    )
    password: str = Field(
        min_length=6,
        max_length=18,
        description="密码",
        examples=["123456"],
    )


# 登录响应模型
class LoginResponse(BaseModel):
    username: str
    is_admin: bool


@app.post(
    "/auth/login",
    summary="用户登录",
    description="用户登录,返回用户信息。",
    tags=["用户"],
    response_description="成功时返回用户信息字典。",
    response_model=LoginResponse,
)
async def login(login_data: LoginRequest):
    if login_data.username == "admin" and login_data.password == "123456":
        return {"username": login_data.username, "is_admin": True}
    else:
        raise HTTPException(status_code=401, detail="用户名或密码错误")


@app.get(
    "/response/html_response",
    summary="返回 HTML 响应",
    description="演示如何返回 HTML 格式的响应内容。",
    tags=["演示"],
    response_description="返回 HTML 格式的字符串内容。",
)
async def html_response():
    html = "<h1>Hello World</h1>"
    return HTMLResponse(content=html)


@app.get(
    "/response/file_response",
    summary="返回文件响应",
    description="演示如何返回文件(如图片)响应,支持浏览器直接预览或下载。",
    tags=["演示"],
    response_description="返回文件二进制流,Content-Type 根据文件类型自动设置。",
)
async def file_response():
    image = "./file/image/001.jpeg"
    return FileResponse(image)
