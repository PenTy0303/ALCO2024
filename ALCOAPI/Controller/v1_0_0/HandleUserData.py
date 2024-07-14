# 標準モジュール
from flask import Blueprint, request, Response
import json
from jsonschema import validate, ValidationError
from logging import getLogger
import os
import datetime
# 自作モジュール
from ALCOAPI.DB.CreateEngine import CreateEngine
from ALCOAPI.DB.makeSession import MakeSession
from ALCOAPI.DB.models import USER, USERData, USERSession

from ALCOAPI.Controller.v1_0_0.CreateHistory import CreateHistory
from ALCOAPI.Controller.v1_0_0.tools import ReadJson, ValidateSessionID

# Blueprint登録
HandleUserData = Blueprint("HandleUesrData", __name__, url_prefix="/ALCOAPI/v1.0.0/HandleUserData")

# loggerの取得
logger = getLogger("MainLog").getChild("HandleUserData")

# グローバル変数の取得
PATH_JSONSCHEMA = "ALCOAPI/Controller/v1_0_0/schema/HandleUesrData_PutUserData.json"

# method

@HandleUserData.route("/<userID>", methods=["GET"])
def HandleUserData_GetUesrData(userID):
    # URLパーサーの戻り値を変換
    input_userID = str(userID)
    
    # アクセス履歴登録
    CreateHistory(REQUEST=request, method="GET", type="HandleUserData_GetUesrData", addition=input_userID)
    
    response = {}
    
    # 送られてきたデータの形式チェック
    try:
        url_args = request.args.to_dict()
        input_sessionID = url_args["sessionID"]
    except KeyError as e:
        logger.debug(f"クエリにsessionIDが含まれません {e}")
        
        return Response(response = json.dumps(""), headers={"Content-Type":"aplication/json"}, status=401)
    
    # 形式チェックが終わったので具体出来な処理を行う
    
    # DBセッションの確立
    try:
        CE = CreateEngine()
        session = MakeSession(CE).getSession()
    except Exception as e:
        logger.debug(f"セッションが確立できませんでした {e}")
        
        return Response(response = json.dumps(""), headers={"Content-Type":"aplication/json"}, status=401)
    
    # セッション有効性のチェック
    if(not ValidateSessionID(session, USERSession, input_sessionID, input_userID)):
        logger.debug(f"sessionIDが不正です")
    
        return Response(response = json.dumps(""), headers={"Content-Type":"aplication/json"}, status=401)
    
    # ユーザーデータの取得を行う
    userData = session.query(USERData).filter(
        session.query(USER).filter(
            USER.userID == input_userID
            ).all()[0].userDataID == USERData.userDataID
        ).all()[0]
    
    # これを形式化して返却する
    response["totalSteps"] = userData.totalSteps
    response["todaySteps"] = userData.todaySteps
    response["point"] = userData.point
    response["favorableRate"] = userData.favorableRate
    response["weekSteps"] = userData.weekSteps
    response["getDate"] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
    
    return Response(response=json.dumps(response), headers={"Content-Type":"aplication/json"}, status=200)

    
    

@HandleUserData.route("/<userID>", methods=["PUT"])
def HandleUserData_PutUesrData(userID):
    userID = str(userID)
    
    return ""


@HandleUserData.route("", methods=["GET"])
def HandleUserData_GetUserDataRanking():
    
    return ""
