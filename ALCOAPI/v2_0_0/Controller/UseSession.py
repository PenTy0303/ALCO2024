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
UseSession = Blueprint("UseSession", __name__,  url_prefix="/ALCOAPI/v2.0.0/UseSession")

# データベースのエンジン作成
CE = CreateEngine.CreateEngine()

# 環境変数の登録
VERSION = os.environ.get("VERSION")

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
    session = makeSession.MakeSession(CE).getSession()
    
    result = ValidateSessionID(session=session, USERSession=models.USERSession, sessionID=input_sessionID, userID=input_userID)
    
    if(result):
        # セッションIDが正常です
        print(Status.get_200(acceptedTime=acceptedTime, body=result))
        return Response(response=json.dumps(Status.get_200(acceptedTime=acceptedTime, body=result)), status=200)
    
    else:
        # セッションIDが不正です
        return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), status=401) 
        
