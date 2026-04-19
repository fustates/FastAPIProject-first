from fastapi import FastAPI

from response import ApiResponse, BusinessError, BizCode, business_error_handler, success

app = FastAPI()
app.add_exception_handler(BusinessError, business_error_handler)


@app.get("/")
async def root() -> ApiResponse:
    return success(data={"message": "Hello World"})


@app.get("/hello/{name}")
async def say_hello(name: str) -> ApiResponse:
    return success(data={"message": f"Hello {name}"})


@app.get("/demo/error")
async def demo_error() -> ApiResponse:
    raise BusinessError("示例业务错误", code=BizCode.NOT_FOUND, http_status=404)
