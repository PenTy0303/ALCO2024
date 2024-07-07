from CreateEngine import CreateEngine
from makeSession import MakeSession
from models import USER, USERData, USERSession, CLIENTHistory
import datetime
import json

def init(session):
    
    d1 = datetime.datetime.now()
    d1_str = d1.strftime('%y-%m-%d %H-%M-%S+09:00')
    
    UserData = USERData(userDataID = "00000000", totalSteps=0, todaySteps=0, point=0, favorableRate=0, reloadedDate = d1_str, weekSteps=json.dumps({"01":100, "02":200, "03":300, "04":400, "05":500, "06":600, "07":700}))
    User = USER(userID = "00000000", auth="administorator", name="masui", password="302c736f670d8be8a9c1aabc4910e4f13e1d1725f1264c06e04294cf6cc239c0", salt="sample", userDataID = "00000000")

    session.add(User)
    session.flush()
    session.add(UserData)
    
    
    session.commit()    

if(__name__ == "__main__"):
    # エンジンの作成
    CE = CreateEngine()
    session = MakeSession(CE).getSession()
    init(session)
    
