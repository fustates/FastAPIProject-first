from typing import Annotated

from fastapi import FastAPI, Path, Query

from response import (
    ApiResponse,
    BusinessError,
    BizCode,
    business_error_handler,
    success,
)

app = FastAPI(
    title="示例 API",
    description="统一响应格式 `{ code, data, msg }` 的 FastAPI 示例服务。",
    version="0.1.0",
    openapi_tags=[
        {"name": "基础", "description": "健康检查与示例接口。"},
        {"name": "图书", "description": "书籍与作者相关查询。"},
        {"name": "演示", "description": "错误与响应格式演示（仅开发环境使用）。"},
    ],
)
app.add_exception_handler(BusinessError, business_error_handler)


@app.get(
    "/",
    summary="根路径",
    description="返回欢迎信息，用于确认服务可用。",
    tags=["基础"],
    response_description="成功时 `code` 为 0，`data` 内含 `message` 字段。",
)
async def root() -> ApiResponse:
    return success(data={"message": "Hello World1233"})


@app.get(
    "/hello/{name}",
    summary="按姓名问候",
    description="根据路径中的姓名返回问候语。",
    tags=["基础"],
    response_description="成功时 `data.message` 为问候内容。",
)
async def say_hello(
    name: Annotated[str, Path(description="要问候的对方姓名")],
) -> ApiResponse:
    return success(data={"message": f"Hello {name}"})


@app.get(
    "/books/{book_id}",
    summary="按编号查询书籍",
    description="通过路径中的书籍编号查询；编号必须为 1～100 之间的整数。",
    tags=["图书"],
    response_description="成功时 `data` 中含 `book_id` 及占位字段。",
)
async def get_book(
    book_id: Annotated[
        int,
        Path(
            ge=1,
            le=100,
            description="书籍编号，取值范围 1～100（含边界）",
        ),
    ],
) -> ApiResponse:
    return success(
        data={"book_id": book_id, "title": None, "note": "示例：此处可接数据库查询"}
    )


@app.get(
    "/authors/{author}",
    summary="按作者查询",
    description="通过路径中的作者名称查询；名称长度须为 2～10 个字符。",
    tags=["图书"],
    response_description="成功时 `data.author` 为路径中的作者名。",
)
async def get_by_author(
    author: Annotated[
        str,
        Path(
            min_length=2,
            max_length=10,
            description="作者名称，长度 2～10 个字符（含边界）",
        ),
    ],
) -> ApiResponse:
    return success(
        data={"author": author, "books": [], "note": "示例：此处可按作者筛选书籍列表"}
    )


@app.get(
    "/news/list",
    summary="获取新闻列表",
    description="分页获取新闻列表，支持指定跳过数量和返回数量。",
    tags=["新闻"],
    response_description="成功时 `data` 中含 `news_list` 及分页信息。",
)
async def get_news_list(
    skip: Annotated[int, Query(ge=0, description="跳过记录数，默认0")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="返回记录数，默认10")] = 10,
) -> ApiResponse:
    # 模拟数据生成，实际项目中应从数据库查询
    news_list = [{"title": f"新闻{i + 1}"} for i in range(skip, skip + limit)]
    return success(
        data={"news_list": news_list, "total": 100, "skip": skip, "limit": limit}
    )


@app.get(
    "/demo/error",
    summary="演示业务错误响应",
    description="故意抛出业务异常，展示统一 JSON 错误体与 HTTP 状态码。",
    tags=["演示"],
    response_description="不会返回 200，响应体仍为 `{ code, data, msg }` 结构。",
)
async def demo_error() -> ApiResponse:
    raise BusinessError("示例业务错误", code=BizCode.NOT_FOUND, http_status=404)
