# sqlalchemyにおけるテーブルのベースクラス
from sqlalchemy.orm import declarative_base

# 制約
from sqlalchemy import ForeignKey

# テーブルの各カラムに対するデータ型
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, BigInteger, DateTime

Base = declarative_base()

# USER テーブル作成
class USER(Base):
    
    # metadata
    __tablename__ = "USER"
    
    # columns
    userID = Column(String(8), primary_key=True, nullable=False, autoincrement=False, unique=True)
    auth = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
    userDataID = Column(String(8), ForeignKey("USERData.userDataID"), nullable=False, unique=True)
    
    # CRUDMethods


# USERDataテーブル作成
class USERData(Base):
    
    # metadata
    __tablename__ = "USERData"
    
    # columns
    userDataID = Column(String(8), primary_key=True, nullable=False, autoincrement=False)
    totalSteps = Column(BigInteger)
    todaySteps = Column(BigInteger)
    point = Column(BigInteger)
    favorableRate = Column(Integer)
    reloadedDate = Column(DateTime)
    weekSteps = Column(String(255))
    
    # CURDMethods

# USERSessionテーブル作成
class USERSession(Base):
    
    # metadata
    __tablename__  = "USERSession"
    
    # columns
    sessionID = Column(String(8), primary_key=True, nullable=False, autoincrement=False)
    userID = Column(String(8), ForeignKey("USER.userID"), nullable=False)
    expiredDate = Column(DateTime, nullable=False)
    state = Column(String(255), nullable=False)
    
    # CRUDMethods

# CLIENTHistoryテーブル作成
class CLIENTHistory(Base):
    
    # metadata
    __tablename__ = "CLIENTHistory"
    
    # columns
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    userID = Column(String(8), ForeignKey("USER.userID"), nullable=False)
    datae = Column(DateTime, nullable=False)
    type = Column(String(255), nullable=False)
    payload = Column(String(1024), nullable=False)
    
    # CRUDMethods



if(__name__ == "__main__"):
    from CreateEngine import CreateEngine
    CE = CreateEngine()
    Base.metadata.create_all(CE.getEngine())