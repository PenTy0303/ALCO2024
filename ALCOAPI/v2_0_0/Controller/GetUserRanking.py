# nomarl module
from flask import Blueprint, request, Response
from jsonschema import validate, ValidationError
from sqlalchemy import desc
from logging import getLogger
import time, json, re, os

# my module
from ..DB import CreateEngine,  makeSession, models
from .CreateHistory import CreateHistory as CH
from .Responses import Responses
from .tools import ValidateSessionID, ReadJson

# initialize

## register blueprint
GetUserRanking = Blueprint("GetUserRanking", __name__, url_prefix="/GetUserRanking")

## get env
VERSION = "v2_0_0"
MAX_INPUT_NUM = 10 # ランキング取得数の上限

## create db engine
CE = CreateEngine.CreateEngine()

## get logger
logger = getLogger("MainLog").getChild("GetUserRanking")

## register re matcher
pattern_userID = r'[a-e0-9]'
matcher_userID = re.compile(pattern_userID)

## instance Resposnses
Status = Responses()

@GetUserRanking.route("/<input_userID>", methods=["get"])
def get_UserRanking(input_userID):
    
    acceptedTime = time.time()
    
    # 履歴の登録
    CH(REQUEST=request, method="GET", type="GetUserRanking", addition=input_userID)
    
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
    
    try:
        input_num = int(request.args["num"])
        
        if(0 > input_num or input_num > MAX_INPUT_NUM):
            raise KeyError 
            
        
    except KeyError:
        input_num = 10
        
    except Exception as e:
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
        user_data_totalSteps : list[tuple] = session.query(models.USER, models.USERData).join(models.USER, models.USER.userDataID == models.USERData.userDataID).order_by(desc(models.USERData.totalSteps)).limit(input_num).all()
        user_data_totalReliefTimes : list[tuple] = session.query(models.USER, models.USERData).join(models.USER, models.USER.userDataID == models.USERData.userDataID).order_by(desc(models.USERData.totalReliefTimes)).limit(input_num).all()
        user_data_currentSeasonReliefTimes : list[tuple] = session.query(models.USER, models.USERData).join(models.USER, models.USER.userDataID == models.USERData.userDataID).order_by(desc(models.USERData.currentSeasonReliefTimes)).limit(input_num).all()
        
        session.close()
        
        body = {}
        body["toalSteps"] = [{"name":i[0].name, "fig":i[1].totalSteps} for i in user_data_totalSteps]
        body["totalReliefTimes"] = [{"name":i[0].name, "fig":i[1].totalReliefTimes} for i in user_data_totalReliefTimes]
        body["currentSeasonReliefTimes"] = [{"name":i[0].name, "fig":i[1].currentSeasonReliefTimes} for i in user_data_currentSeasonReliefTimes]
        
    except Exception as e:
        
        session.rollback()
        session.close()
        
        logger.debug("データベース関連でエラーが発生しました:%s" % (e))
        return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), status=401, headers={"Content-Type":"application/json"})
        
    return Response(response=json.dumps(Status.get_200(acceptedTime=acceptedTime, body=body)), status=200, headers={"Content-Type":"application/json"})   
        
        