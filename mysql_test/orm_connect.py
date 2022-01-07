'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-12-31 16:17:11
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-01-04 10:57:24
'''
from sqlalchemy import create_engine
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.visitors import TraversibleType

# 准备链接
engine = create_engine('mysql://root:3232636521tuot@127.0.0.1:3306/learn_orm?charset=utf8',
                       echo=True)

# 声明ORM模型的基类
Base = declarative_base()


class Student(Base):
    """ 学生信息表 """
    __tablename__ = 'student'
    id = Column(type_=Integer, name='id', primary_key=True)
    stu_no = Column(type_=Integer, nullable=False, comment='学号')
    stu_name = Column(type_=String(16), nullable=False, comment='姓名')
    created_at = Column(type_=DateTime)


def create_table():
    Base.metadata.create_all(bind=engine)
