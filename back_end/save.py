from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 定义work类作为数据库模版表格
class Work(Base):
    __tablename__ = "works"
    # 唯一标识
    id = Column(Integer, primary_key=True)
    # title
    title_text = Column(String)
    # 确保该url在关键词搜索下只出现一次
    title_url = Column(String, unique=True, index=True)

    # author
    author_text = Column(String)
    author_url = Column(String)

    # tags
    tags = Column(Text)
