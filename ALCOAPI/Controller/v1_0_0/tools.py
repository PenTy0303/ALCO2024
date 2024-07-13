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
                
    
    
    
    
