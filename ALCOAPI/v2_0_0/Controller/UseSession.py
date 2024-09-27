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
UseSession = Blueprint("UseSession", __name__,  url_prefix="/UseSession")

# データベースのエンジン作成
CE = CreateEngine.CreateEngine()

# 環境変数の登録
VERSION = "v2_0_0"

# loggerの取得
logger = getLogger("MainLog").getChild("UseSession")

# 正規表現の登録
pattern_userID = r'[a-z0-9]'
matcher_userID = re.compile(pattern_userID)

# レスポンスクラスの登録

Status = Responses()

# router
@UseSession.route("/<input_userID>", methods=["get"])
def get_UseSession(input_userID):
    
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
        return Response(response=json.dumps(Status.get_401()), headers={"Content-Type":"application/json"})
    
    result = ValidateSessionID(session=session, USERSession=models.USERSession, sessionID=input_sessionID, userID=input_userID)
    
    if(result):
        # セッションIDが正常です
        # print(Status.get_200(acceptedTime=acceptedTime, body=result))
        return Response(response=json.dumps(Status.get_200(acceptedTime=acceptedTime, body=result)), status=200)
    
    else:
        # セッションIDが不正です
        return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), status=401) 
        
@UseSession.route("/<input_userID>", methods=["delete"])
def delete_UseSession(input_userID):
    
    acceptedTime = time.time()
    
    # 履歴の登録
    CH(REQUEST=request, method="DELETE", type="DeleteUseSession", addition=input_userID)
   
    # 入力データのヴァリデーション
    if(not matcher_userID.match(input_userID)):
        logger.debug("userIDが不正です")
        return Response(status=401, response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), headers={"Content-Type":"application/json"})
    
    try:
        input_sessionID = request.args["sessionID"]
        if(not matcher_userID.match(input_sessionID)):
            return Response(status=401, response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), headers={"Content-Type":"application/json"})
        
    except Exception as e:
        logger.debug("sessionIDが不正です")
        return Response(status=401, response=json.dumps(Status.get_404(acceptedTime=acceptedTime)), headers={"Content-Type":"application/json"})
    
    # 入力データのバリデーション終了
    
    # DBとの接続開始
    try:
        session = makeSession.MakeSession(CE=CE).getSession()
    except:
        logger.debug("データベースとの接続に失敗しました")
        return Response(status=401, response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), headers={"Content-Type":"application/json"})
    
    # sessionIDの認証を行います
    if(not ValidateSessionID(session, models.USERSession, input_sessionID, input_userID)):
        logger.debug("認証に失敗しました")
        return Response(status=401, response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), headers={"Content-Type":"application/json"})
    
    try:
        # 認証が通過したsessionIDを削除します
        found_account = session.query(models.USERSession).filter(models.USERSession.sessionID == input_sessionID).first()
        
        # 実際に削除
        session.delete(found_account)
        
        # コミットs
        session.commit()
    except Exception as e:
        
        # 異常終了した場合はロールバックする
        session.rollback()
        
        logger.debug("何かしらがうまくいかなかった%s" % (e))
        
        
        session.close()
        return Response(status=401, response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), headers={"Content-Type":"application/json"})

    # すべての動作が正常に終了した
    
    return Response(status=200, response=json.dumps(Status.get_200(acceptedTime=acceptedTime)), headers={"Content-Type":"application/json"})