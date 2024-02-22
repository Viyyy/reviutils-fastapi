from pydantic import BaseModel, EmailStr
from typing import Union

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    mobile_phone: str
    role: str
    disabled: bool

class UserInDB(User):
    hashed_password: str