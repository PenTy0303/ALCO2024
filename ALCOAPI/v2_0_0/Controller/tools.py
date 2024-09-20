# 標準モジュール
import json
import hashlib
import random
import string
import datetime
from sqlalchemy.orm import sessionmaker
from ..DB import models
import time


# グローバル変数
DATE_FORMAT = "%Y/%m/%d %H:%M:%S.%s"

# 自作モジュール

# JSONを読み込む
def ReadJson(path):
    with open(path, mode = "r") as f:
        response = json.load(f)
        
    return response

# 文字列をSHA256でハッシュ化する
def HashText(*text):
    # 文字列結合
    joinedText = "".join(text).encode('utf-8')
    
    # ハッシュ化
    hashedText = hashlib.sha256(joinedText)
    
    # 16進数化したものを返却
    return hashedText.hexdigest()

# UUIDを生成する（内部）
def _CreateUUID(num = 8):
    x = lambda: string.hexdigits[random.randint(0, 15)]
    h = lambda: "".join([x() for _ in range(0, num)])
    
    return h()

# セッションIDを作成及び，チェックを行う
def GetSessionID(session, userSession, userID):
    
    table = userSession
    
    # 同様のIDが他にあるかどうかをチェック
    result = session.query(table).filter(table.userID == userID).all()
    
    # 返却結果が0であればそのuserIDは他に存在しないので新規生成．
    if(len(result) == 0):
        while(True):
            pre_sessionID = _CreateUUID(8)
            
            if(len([True for i in result if i["sessionID"]==pre_sessionID]) == 0):
                sessionID = pre_sessionID
                break
        
        userSession = table()
           
        userSession.userID = userID
        userSession.sessionID = sessionID
        userSession.expiredDate = datetime.datetime.now() + datetime.timedelta(days=7)
        userSession.state = "available"
        
        session.add(userSession)

    else:
        result = result[0]
        
        sessionID = result.sessionID
        result.expiredDate = datetime.datetime.now() + datetime.timedelta(days=7)
        result.state = "available"
        
    
    session.commit()
        
    return sessionID

# UESRIDを発行する
def CreateUserID(session, user, userData):
    
    # 現在のテーブル状況を取得
    current_user = session.query(user).all()
    current_userData = session.query(userData).all()
    
    # userIDを重複しないように発行
    while(True):
        userID = _CreateUUID(8)
        
        if(len([True for i in current_user if i.userID == userID]) == 0):
            break
    
    # USERDataIDを発行する
    while(True):
        userDataID = _CreateUUID(8)
        
        if(len([True for i in current_userData if i.userDataID == userDataID]) == 0):
            break
        
    # 発行したものを返却する
    
    return {"userID":userID, "userDataID":userDataID}
    

# 文字列同士の比較をセキュアに行う
def VerifyString(base, target, min_length=-1):
    base_length = len(base)
    target_length = len(target)
    
    if(base_length > target_length):
        length = base_length
    else:
        length = target_length
    flag = True
    
    # そもそもmin_lengthが指定されていないか，検索の最小回数lengthを超えていないため，最小回数で実行する
    if(min_length == -1 and length > min_length):
        for i in range(length):
            try:
                if(base[i] != target[i]):
                    flag = False
            except IndexError as e:
                flag = False
                    
    # 所定の回数確実に比較を行う．
    else:
        for i in range(min_length):
            try:
                if(base[i] != target[i]):
                    flag = False
            except:
                flag = False
    
    # 判定結果はflagに格納されている．
    return flag
                

# sessionIDの有効性をチェックする
def ValidateSessionID(session, USERSession, sessionID, userID):
    
    # USERSessionの現在の状態を取得
    current_USERSession = session.query(USERSession).all()
    
    # その中からsessionIDによるカラムを取得
    current_session = [i for i in current_USERSession if i.sessionID == sessionID]
    
    if(len(current_session) == 0):
        # sessionIDが存在しない
        return False
    
    current_session = current_session[0]
    
    # そのセッションの状態をチェックする
    if(current_session.state == "available"):
        # そのセッションが有効時間内かどうかをチェックする
        
        expiredDate =current_session.expiredDate
        # 期限内であった場合
        if(datetime.datetime.now() <= expiredDate):
            
            # そのセッションがuserIDによるものかどうかをチェックする
            if(current_session.userID == userID):
                # そのセッションは有効である
                
                # 時間の更新を行う
                current_session.expiredDate = datetime.datetime.now() + datetime.timedelta(days=7)
                session.commit()
                
                return {"sessionID": sessionID, "expireDate": datetime.datetime.timestamp(current_session.expiredDate)}
    
    # セッションは有効ではなかったことを示す       
    return None


# 地球の状態を初期状態に戻す
# どんな数値にするかはここで管理する
def ResetEarthStatus(session : sessionmaker , USERData : models.USERData , userID : str):
    
    class DefaultStatus():
        DESTRUCTION_RATE : int = 75
        CIVILIZATION_RATE : int = 25
        DEBUFF : int = 0
        
    DS = DefaultStatus()
    try:
        user_data : list[models.USERData] = session\
                .query(models.USER, models.USERData)\
                .join(models.USERData, models.USER.userDataID == models.USERData.userDataID)\
                .filter(models.USER.userID == userID)\
                .first()
        
        ## 初期値のセット
                
        user_data[1].destructionRate = DS.DESTRUCTION_RATE
        user_data[1].civilizationRate = DS.CIVILIZATION_RATE
        user_data[1].currentDebuff = DS.DEBUFF
        user_data[1].currentSeasonReliefTimes = 0
        user_data[1].lastReliefTimesUpdate = time.time()
        
        ## 救済期限の変更
        dt = datetime.datetime.now()
        ltddt = datetime.datetime(year=dt.year, month=dt.month, day=dt.day+7+(7-dt.weekday()), hour=0, minute=0, second=0, microsecond=0)    
        
        user_data[1].ltdReliefDate = int(ltddt.timestamp())

        session.commit()
        
    except Exception as e:
        
        raise Exception
        
        
        