from utils.auth import crud
from utils.auth.models import User
from utils.auth.database import SessionLocal, Base, engine
from passlib.context import CryptContext

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# region 创建一个管理员账号
admin = User()
admin.username = 'reviy'
admin.full_name = 'Reviy.top'
admin.email = 'reviy-top@outlook.com'
admin.mobile_phone = '12345678901'
admin.role = 'Admin'# 这里可以用其他方法设置权限
admin.hashed_password = pwd_context.hash('admin') # 请设置一个难一点的密码

with SessionLocal() as db:
    user = crud.add_user(db, admin)
# endregion