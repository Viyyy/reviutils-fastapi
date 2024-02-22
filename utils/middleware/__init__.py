import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})

class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        execution_time = end_time - start_time
        response.headers["X-Response-Time"] = str(execution_time)
        return response