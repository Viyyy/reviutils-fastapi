
from utils.auth import default_auth_helper as auth_helper
from fastapi import APIRouter

router = APIRouter()

auth_helper.add_tokenUrl_to(router)

@router.get('/user/me')
async def me(token: str = auth_helper.dependency):
    user = auth_helper.get_current_user(token)
    if user is None:
        raise auth_helper.unauthorised('无法验证凭据')
    return f'Hello, {user.full_name}'