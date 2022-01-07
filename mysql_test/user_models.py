'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-01-05 15:05:56
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-01-05 16:02:04
'''
from datetime import datetime
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy import Column, String, Integer, SmallInteger, DateTime, Boolean, Enum
from sqlalchemy.dialects.mysql import CHAR, TINYINT
from enum import IntEnum


Base = declarative_base()


class sexEnum(IntEnum):
    MAN = 1   # 男
    WOMEN = 2  # 女


class User(Base):
    ''' 用户信息表 '''
    __tablename__ = 'account_user'
    id = Column('id', type_=Integer, primary_key=True)
    username = Column('username', type_=String(
        32), nullable=False, unique=True, comment='用户名')
    password = Column('password', type_=String(512),
                      nullable=False, comment='密码')
    real_name = Column('real_name', type_=String(16), comment='真实姓名')
    sex = Column('sex', type_=Enum(sexEnum), default=None, comment='性别')
    age = Column('age', type_=TINYINT(unsigned=True), default=0, comment='年龄')
    created_at = Column('created_at', type_=DateTime,
                        default=datetime.now(), comment='创建时间')
    is_valid = Column('is_valid', type_=Boolean, default=True, comment='是否有效')


class UserAddress(Base):
    ''' 地址信息表 '''
    __tablename__ = 'account_user_address'

    id = Column(Integer, primary_key=True)
    area = Column(String(256), nullable=False, comment='地址信息')
    phone_no = Column(CHAR(11), comment='电话号码')
    remark = Column(String(256), comment='备注信息')
    is_valid = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
