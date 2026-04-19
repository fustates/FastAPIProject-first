"""统一 API 响应格式 { code, data, msg } 与业务状态码。"""

from __future__ import annotations

from enum import IntEnum
from typing import Any, TypeVar

from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

T = TypeVar("T")


class BizCode(IntEnum):
    """业务状态码：0 成功；非 0 表示各类业务错误，可按模块分段编号便于管理。"""

    SUCCESS = 0

    # 客户端 / 参数（示例区间 4xxxx）
    BAD_REQUEST = 40000
    UNAUTHORIZED = 40100
    FORBIDDEN = 40300
    NOT_FOUND = 40400

    # 服务端（示例区间 5xxxx）
    INTERNAL_ERROR = 50000


class ApiResponse(BaseModel, frozen=True):
    """固定外层结构，便于前端与网关统一处理。"""

    code: int = Field(description="业务状态码，0 表示成功")
    data: Any = Field(default=None, description="业务数据")
    msg: str = Field(default="", description="说明信息")


def success(data: Any = None, msg: str = "ok") -> ApiResponse:
    return ApiResponse(code=int(BizCode.SUCCESS), data=data, msg=msg)


def fail(
    code: BizCode | int,
    msg: str,
    data: Any = None,
) -> ApiResponse:
    c = int(code) if isinstance(code, BizCode) else code
    return ApiResponse(code=c, data=data, msg=msg)


class BusinessError(Exception):
    """在路由里 raise，由全局异常处理转为统一 JSON 结构。"""

    def __init__(
        self,
        msg: str,
        *,
        code: BizCode | int = BizCode.BAD_REQUEST,
        data: Any = None,
        http_status: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        self.code = int(code) if isinstance(code, BizCode) else code
        self.msg = msg
        self.data = data
        self.http_status = http_status
        super().__init__(msg)


async def business_error_handler(_: Request, exc: BusinessError) -> JSONResponse:
    body = fail(exc.code, exc.msg, exc.data).model_dump()
    return JSONResponse(status_code=exc.http_status, content=body)
