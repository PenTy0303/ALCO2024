# 標準モジュール
from flask import Blueprint, request, Response
from logging import getLogger
import re
import os
import json
import time

# 自作モジュール
from ..DB import CreateEngine, makeSession, models
from .CreateHistory import CreateHistory as CH
from .Responses import Responses
from .tools import ValidateSessionID

# BluePrintの登録
InterfereTime = Blueprint("InterfereTime", __name__,  url_prefix="/ALCOAPI/v2.0.0/InterfereTime")

# データベースのエンジン作成
CE = CreateEngine.CreateEngine()

# 環境変数の登録
VERSION = os.environ.get("VERSION")

# loggerの取得
logger = getLogger("MainLog").getChild("InterfereTime")

# 正規表現の登録
pattern_userID = r'[a-z0-9]'
matcher_userID = re.compile(pattern_userID)

# レスポンスクラスの登録

Status = Responses()

# lastInterfereDateと現在時刻の差を求めてそれをレスポンスする
@InterfereTime.route("/<input_userID>", methods=["get"])
def get_InterfereTime(input_userID):
    
    acceptedTime = time.time()
    
    # 履歴の登録
    CH(REQUEST=request, method="GET", type="GetUseSession", addition=input_userID)
    
    # 入力データのヴァリデーション
    if(not matcher_userID.match(input_userID)):
        logger.debug("userIDが不正です")
        return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), status=401)

    try:
        if(not matcher_userID.match(request.args["sessionID"])):
            logger.debug("sessionIDが不正です")
            return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), status=401)
        
    except Exception:
        logger.debug("sessionIDが存在していません")
        return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), status=401)
    
    # 入力データのセット
    input_sessionID = request.args["sessionID"]
    
    # セッションの判定
    try:
        session = makeSession.MakeSession(CE=CE).getSession()
    except:
        return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), headers={"Content-Type":"application/json"})
    
    # この変数にセッションの判定結果を格納する
    result = ValidateSessionID(session=session, USERSession=models.USERSession, sessionID=input_sessionID, userID=input_userID)
    
    
    # セッションが不正の場合，取得しない
    if(not result):
        return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), status=401, headers={"Content-Type":"application/json"})
    
    try:
        # 最終干渉時間取得
        lastInterfereTime = session.query(models.USER, models.USERData)\
                            .join(models.USERData, models.USERData.userDataID == models.USER.userDataID)\
                            .filter(models.USER.userID == input_userID)\
                            .first()[1]\
                            .lastInterfereDate
        
        lastInterfereTime = int(lastInterfereTime)
                            
        # 現在時刻取得
        current_time = time.time()
        
    except Exception as e:
        
        session.rollback()
        session.close()
        
        
        logger.debug("データベース関連でエラーが発生しました:%s" % (e))
        return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), status=401, headers={"Content-Type":"application/json"})
    
    finally:
        
        session.close()
    
    return Response(response=json.dumps(Status.get_200(acceptedTime=acceptedTime, body={"nonInterfereTime": str(current_time - lastInterfereTime)})), status=200, headers={"Content-Type":"application/json"})
    
# lastInterfereDataを現在時刻に更新する
@InterfereTime.route("/<input_userID>", methods=["put"])
def put_InterfereTime(input_userID):
    acceptedTime = time.time()
    
    # 履歴の登録
    CH(REQUEST=request, method="GET", type="GetUseSession", addition=input_userID)
    
    # 入力データのヴァリデーション
    if(not matcher_userID.match(input_userID)):
        logger.debug("userIDが不正です")
        return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), status=401)

    try:
        if(not matcher_userID.match(request.args["sessionID"])):
            logger.debug("sessionIDが不正です")
            return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), status=401)
        
    except Exception:
        logger.debug("sessionIDが存在していません")
        return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), status=401)
    
    # 入力データのセット
    input_sessionID = request.args["sessionID"]
    
    # セッションの判定
    try:
        session = makeSession.MakeSession(CE=CE).getSession()
    except:
        return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), headers={"Content-Type":"application/json"})
    
    # この変数にセッションの判定結果を格納する
    result = ValidateSessionID(session=session, USERSession=models.USERSession, sessionID=input_sessionID, userID=input_userID)
    
    
    # セッションが不正の場合，取得しない
    if(not result):
        return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), status=401, headers={"Content-Type":"application/json"})
    
    try:
        lastInterfereTime = session\
                            .query(models.USER, models.USERData)\
                            .join(models.USERData, models.USERData.userDataID == models.USER.userDataID)\
                            .filter(models.USER.userID == input_userID)\
                            .first()

        lastInterfereTime[1].lastInterfereDate = time.time()
        
        session.commit()
        
    except Exception as e:
        
        session.rollback()
        session.close()
        
        logger.debug("データベース関連でエラーが発生しました:%s" % (e))
        return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), status=401, headers={"Content-Type":"application/json"})
    
    finally:
        
        session.close()
        
    return Response(response=json.dumps(Status.get_200(acceptedTime=acceptedTime)), status=200, headers={"Content-Type":"application/json"})    