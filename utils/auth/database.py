from utils.database import *
from configs import webConfig

# DATABASE_RELATIVE_PATH = ''
SQLALCHEMY_DATABASE_URL = webConfig.sqlite_db['auth']['url']
engine = get_sqlite_engine(SQLALCHEMY_DATABASE_URL)

Base = get_engine_base(db_name='auth', name='AuthBase')

SessionLocal = get_local_session(engine=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()