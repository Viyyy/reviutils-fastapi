from sqlalchemy.orm import Session
from traceback import print_exc
from .models import User

def get_user(db:Session, username:str):
    '''根据用户名查询用户'''
    try:
        user = db.query(User).filter(User.username==username).first()
        if user:
            return user
    except:
        print_exc()
        
def add_user(db:Session, new_user:User):
    '''新增用户'''
    try:
        user = db.query(User).filter(User.username==new_user.username).first()
        if not user:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
    except:
        print_exc()