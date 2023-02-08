from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import ExceptionMiddleware
from mangum import Mangum
from .utils.power_tools import logger
from .routers.logging_router import LoggerRouteHandler
import uvicorn
import os

app = FastAPI()
app.router.route_class = LoggerRouteHandler
app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)


@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    # Get correlation id from X-Correlation-Id header
    corr_id = request.headers.get("x-correlation-id")
    if not corr_id:
        # If empty, use request id from aws context
        corr_id = request.scope["aws.context"].aws_request_id

    # Add correlation id to logs
    logger.set_correlation_id(corr_id)

    response = await call_next(request)

    # Return correlation header in response
    response.headers["X-Correlation-Id"] = corr_id
    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(request, err):
    logger.exception("Unhandled exception")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@app.get("/")
def get_root():
    POWERTOOLS_SERVICE_NAME = os.environ.get("POWERTOOLS_SERVICE_NAME")
    logger.info(f"Test fastapi with aws powertools {POWERTOOLS_SERVICE_NAME}")
    return {"message": "FastAPI running in a lambda function"}


handler = Mangum(app)
handler = logger.inject_lambda_context(handler, clear_state=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
