from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 自动生成与uvicorn启动目录相同的文件
DATABASE_URL = "sqlite:///./ao3.db"

# 写明数据库路径
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
