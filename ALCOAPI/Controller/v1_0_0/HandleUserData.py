# 標準モジュール
from flask import Blueprint, request, Response
import json
from jsonschema import validate, ValidationError
from logging import getLogger
import os
import datetime
import re

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

PATTERN_NUM = re.compile(r'[0-9]')
MAX_LOWEST = 10

# RankedItemの定義
# 0 USERData.totalSteps, 1 USERData.todaySteps, 2 USERData.point, 3 USERData.favirableRate
# もしランキング対象が増えることがあれば，ここに合わせて記述する
RANKED_ITEMS = {
                "0000":[0, 1, 2, 3], 
                "0001":[0], 
                "0002":[1], 
                "0003":[2], 
                "0004":[3]
               }

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
    
    # 履歴の登録
    CreateHistory(REQUEST=request, method="GET", type="HandleUserData_GetUserDataRanking")
    
    response = {}
    
    # クエリを取得
    try:
        input_RankedItem = request.args["RankedItem"]
    except KeyError as e:
        logger.debug(f"クエリが正確ではありません {e}")
        
        return Response(response=json.dumps(""), headers={"Content-Type":"aplication/json"}, status=401)
        
    # RankedItemが指定のものかどうか    
    if(not input_RankedItem in RANKED_ITEMS.keys()):
        return Response(response=json.dumps(""), headers={"Content-Type":"aplication/json"}, status=401)
    
    # input_lowertは数値かどうか
    
    try:
        input_lowest = request.args["lowest"]
        if(PATTERN_NUM.search(input_lowest)):
            # 数値に変換して004等の入力を4に変換する
            input_lowest = int(input_lowest)
            
            # もし，MAX_LOWESTの値を超えてしまった場合はその値で抑える
            input_lowest = input_lowest if input_lowest < MAX_LOWEST else MAX_LOWEST
        else:
            return Response(response=json.dumps(""), headers={"Content-Type":"aplication/json"}, status=401)
        
    except KeyError:
        input_lowest = 5
    
    # クエリの形式は正常でなので，具体的な処理に移る
    
    # DBセションを確立する
    try:
        CE = CreateEngine()
        session = MakeSession(CE).getSession()
    except Exception as e:
        logger.debug(f"セッションが確立できませんでした {e}")
        
        return Response(response = json.dumps(""), headers={"Content-Type":"aplication/json"}, status=401)
    
    # データを取得する
    response["length"] = len(RANKED_ITEMS[input_RankedItem])
    response["responses"] = []
    
    # データの書き込み
    for col in RANKED_ITEMS[input_RankedItem]:
        tmp_result = {}
        
        # orderbyの対象を分割して処理を変える
        if(col == 0):
            # col=0はtotalStepsでOrderBy
            
            tmp_result["RankedItem"] = "totalSteps"
            
            userData = session.query(USER,USERData).\
                join(USER, USER.userDataID == USERData.userDataID).\
                order_by(USERData.totalSteps).\
                limit(input_lowest).\
                all()
                
            print("dfsf" , userData[0])
            
            tmp_result["length"] = len(userData)
            tmp_result["data"] = [{"name":i[0].name, "data":i[1].totalSteps} for i in userData]
            
            
        
        elif (col == 1):
            # col=1はtodayStepsでOrderBy
            
            tmp_result["RankedItem"] = "todaySteps"
            
            userData = session.query(USER,USERData).\
                join(USER, USER.userDataID == USERData.userDataID).\
                order_by(USERData.todaySteps).\
                limit(input_lowest).\
                all()
            
            print(userData[0])
            
            tmp_result["length"] = len(userData)
            tmp_result["data"] = [{"name":i[0].name, "data":i[1].todaySteps} for i in userData]
            
            
            
        elif (col == 2):
            # col=2はpointでOrderBy
            
            tmp_result["RankedItem"] = "point"
            
            userData = session.query(USER,USERData).\
                join(USER, USER.userDataID == USERData.userDataID).\
                order_by(USERData.point).\
                limit(input_lowest).\
                all()
            
            tmp_result["length"] = len(userData)
            tmp_result["data"] = [{"name":i[0].name, "data":i[1].point} for i in userData]
            
            
        
        elif (col == 3):
            # col=3はfavorableRateでOrderBy
            
            tmp_result["RankedItem"] = "favorableRate"
            
            userData = session.query(USER,USERData).\
                join(USER, USER.userDataID == USERData.userDataID).\
                order_by(USERData.favorableRate).\
                limit(input_lowest).\
                all()
            
            tmp_result["length"] = len(userData)
            tmp_result["data"] = [{"name":i[0].name, "data":i[1].favorableRate} for i in userData]
            
        response["responses"].append(tmp_result)
        
    
    return Response(response=json.dumps(response), headers={"Content-Type": "application/json"}, status=200)
