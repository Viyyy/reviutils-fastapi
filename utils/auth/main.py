from .database import Base,SessionLocal,engine
import utils.auth.schemas as schemas
import utils.auth.models as models
import utils.auth.crud as crud
from configs import webConfig

from typing import Union
from fastapi import HTTPException, status, Depends, FastAPI, APIRouter
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
Base.metadata.create_all(bind=engine)

# 加密方法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 密钥，cmd输入获取：openssl rand -hex 32
SECRET_KEY = webConfig.auth['SECRET_KEY']
ALGORITHM = 'HS256'
# TOKEN有效时长
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthHelper:
    ''' OAuth2认证管理
    :param app: FastAPI或APIRouter应用
    :param tags: api标签
    :param tokenUrl: 用于获取验证token的Url
    '''
    def __init__(self,
        tokenUrl:str='login', 
        secret_key:str = SECRET_KEY,  
        algorithm:str = ALGORITHM,
        expire_min: int = ACCESS_TOKEN_EXPIRE_MINUTES,
        pwd_context:CryptContext=pwd_context,
        session:Session=SessionLocal,
        prefix:str=None
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_min = expire_min
        if prefix:
            tokenUrl = prefix+"/"+tokenUrl
        self.tokenUrl = "/" + tokenUrl
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=tokenUrl)
        self.pwd_context = pwd_context
        self.session = session

    def unauthorised(self, detail:str = "Incorrect username or password"):
        return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )
        
    @property
    def dependency(self):
        return Depends(self.oauth2_scheme)
        
    def verify_password(self, plain_password, hashed_password):
        '''验证密码'''
        result = self.pwd_context.verify(plain_password, hashed_password)
        return result
    
    def get_password_hash(self, password):
        '''加密密码'''
        hpwd = self.pwd_context.hash(password)
        return hpwd
        
    def get_user(self, username:str)->models.User:
        '''获取用户'''
        with self.session() as db:
            user = crud.get_user(db, username)
            if user:
                return user
            
    def add_user(self, new_user:schemas.UserInDB):
        '''新增用户'''
        new_user.hashed_password = self.get_password_hash(new_user.hashed_password)
        new_user_dict = new_user.model_dump()
        new_user = models.User(**new_user_dict)
        with self.session() as db:
            user = crud.add_user(db, new_user)
            return user
        
    def authenticate_user(self, username: str, password: str):
        '''认证用户'''
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user
        
    def create_access_token(self, data: dict, expires_delta: Union[timedelta, None] = None):
        '''生成token'''
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.expire_min)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def login_for_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        '''登录获取token'''
        user = self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise self.unauthorised()
        access_token_expires = timedelta(minutes=self.expire_min)
        access_token = self.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    def add_tokenUrl_to(self, app:Union[FastAPI,APIRouter], tags=['OAuth2认证']):
        '''添加【获取token的路由】到app或router'''
        app.add_api_route(self.tokenUrl, self.login_for_access_token, tags=tags, methods=['POST'], response_model=schemas.Token)
        
    def get_current_user(self, token:str):
        credentials_exception = self.unauthorised("无法验证凭据")
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = schemas.TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
    
default_auth_helper = AuthHelper()