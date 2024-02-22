from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from .database import Base

class User(Base):
    __tablename__='user'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    username = Column(String(20), nullable=False, unique=True, comment='用户名')
    full_name = Column(String(50), nullable=False, comment='全名')
    email = Column(String(100), nullable=False, comment='用户邮箱')
    mobile_phone = Column(String(11), nullable=False, comment='手机号')
    role = Column(String(15),nullable=False, comment='角色名')
    disabled = Column(Boolean, nullable=False, default=False, comment='是否禁用')
    
    hashed_password = Column(String(100), nullable=False, comment='加密的密码')
    
    createdAt = Column(DateTime, server_default=func.now(),comment='创建时间')
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(),comment='更新时间')