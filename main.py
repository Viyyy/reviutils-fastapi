from configs import webConfig

from fastapi import FastAPI
app = FastAPI(
    **webConfig.app['config'],
)

#region OAuth2认证
from utils.auth import default_auth_helper as auth_helper
from utils.auth.schemas import User, UserInDB
from fastapi import Depends,status,HTTPException
auth_helper.add_tokenUrl_to(app)

async def get_current_user(token: str = auth_helper.dependency):
    return auth_helper.get_current_user(token)

@app.get("/Oauth2Test",tags=['OAuth2认证'],dependencies=[auth_helper.dependency])
def oauth2Test():
    '''OAuth2测试'''
    return webConfig.app['config']['title']+": oauth2测试"

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="用户不可用")
    return current_user

@app.get("/users/me/", response_model=User, tags=['OAuth2认证'])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    '''获取当前用户，OAuth2认证'''
    return current_user

@app.post('/users/new/', response_model=User, tags=['OAuth2认证'])
async def add_user(new_user:UserInDB, current_user: User = Depends(get_current_user)):
    '''新增用户'''
    if current_user.role!='Admin':
        raise auth_helper.unauthorised('该角色权限不足')
    user = auth_helper.add_user(new_user)
    if user is None: 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='新增用户失败',
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user
#endregion

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
from utils.router import RouterManager, Router
routers = [
    Router(name='index', prefix='Index', tags='在绑定路由时添加OAuth2',dependencies=[auth_helper.dependency]),
    Router(name='auth', prefix='Auth', tags='在路由里添加OAuth2'),
]

ROUTER_MANAGER = RouterManager(routers)
ROUTER_MANAGER.add_routers_to(app)
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