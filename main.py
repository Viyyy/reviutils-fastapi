from configs import webConfig

from fastapi import FastAPI
app = FastAPI(
    **webConfig.app['config'],
)

# region 设置跨域与中间件
from fastapi.middleware.cors import CORSMiddleware
import utils.middleware as middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = webConfig.cors['allow_origins'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.add_middleware(middleware.ExceptionMiddleware)
app.add_middleware(middleware.TimerMiddleware)
# endregion

#region 添加路由
from applications.reviutils import router as reviutils_router
app.include_router(reviutils_router, tags=['reviutils-fastapi接口实现'])
#endregion

# region 忽略警告
import warnings
warnings.filterwarnings("ignore")
# endregion

if __name__=='__main__':
    import uvicorn
    uvicorn.run(
        app="main:app",
        **webConfig.server
    )