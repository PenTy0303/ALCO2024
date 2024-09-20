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
ReliefTime = Blueprint("ReliefTime", __name__,  url_prefix="/IsRelief")

# データベースのエンジン作成
CE = CreateEngine.CreateEngine()

# 環境変数の登録
VERSION = "v2_0_0"

# loggerの取得
logger = getLogger("MainLog").getChild("ReliefTime")

# 正規表現の登録
pattern_userID = r'[a-z0-9]'
matcher_userID = re.compile(pattern_userID)

# レスポンスクラスの登録

Status = Responses()

# ハンドラー

@ReliefTime.route("/<input_userID>", methods=["get"])
def get_ReliefTime(input_userID):

    acceptedTime = time.time()
    
    # 履歴の登録
    CH(REQUEST=request, method="GET", type="GetReliefTime", addition=input_userID)
    
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
    
    # 地球の救済を判定する
    
    try:
            sql_response = session.query(models.USER, models.USERData).join(models.USER, models.USER.userDataID == models.USERData.userDataID).filter(models.USER.userID == input_userID).first()
            ltdReliefDate : int = sql_response[1].ltdReliefDate # UnixTimeで格納されているデータを扱う
            
            isRelief = True
            
            # 期限の時間より今のほうが大きいということは期限を過ぎているということ
            if(ltdReliefDate < time.time()):
                isRelief = False
            
            session.close()

            
            return Response(response=json.dumps(Status.get_200(acceptedTime=acceptedTime, body={"isRelief":isRelief})), status=200, headers={"Content-Type":"application/json"})
    except Exception as e:
        session.close()
        
        logger.debug("データーベース関連に以上が発生しました %s" % (e))
        
        return Response(response=json.dumps(Status.get_404(acceptedTime=acceptedTime)), headers={"Content-Type":"application/json"}, status=404)
    
    