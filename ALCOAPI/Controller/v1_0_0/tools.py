# 標準モジュール
import json
import hashlib
import random
import string
import datetime


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
def GetSessionID(session, table, userID):
    
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
    
    
    
    
