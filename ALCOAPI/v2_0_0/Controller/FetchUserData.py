# nomarl module
from flask import Blueprint, request, Response
from jsonschema import validate, ValidationError
from logging import getLogger
import time, json, re, os

# my module
from ..DB import CreateEngine,  makeSession, models
from .CreateHistory import CreateHistory as CH
from .Responses import Responses
from .tools import ValidateSessionID, ReadJson

# initialize

## register blueprint
FetchUserData = Blueprint("FetchUserData", __name__, url_prefix="/ALCOAPI/v2.0.0/FetchUserData")

## get env
VERSION = os.environ.get("VERSION")

## create db engine
CE = CreateEngine.CreateEngine()

## get logger
logger = getLogger("MainLog").getChild("FetchUserData")

## register re matcher
pattern_userID = r'[a-e0-9]'
matcher_userID = re.compile(pattern_userID)

## json schema path
PATH_SCHEMA = f"ALCOAPI/{VERSION}/Controller/schema/FetchUserData_put.json"

## instance Resposnses
Status = Responses()

# router
@FetchUserData.route("/<input_userID>", methods=["get"])
def get_FetchUserData(input_userID):
    
    acceptedTime = time.time()
    
    CH(REQUEST=request, method="GET", type="GetFetchUserData")
    
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
    
    # データの取得を開始
    try:
        user_data : tuple = session.query(models.USER, models.USERData).join(models.USERData, models.USER.userDataID == models.USERData.userDataID).filter(models.USER.userID == input_userID).first()

    except Exception as e:
        logger.debug(f"データベースの接続中にエラーが発生しました : {e}")
        return Response(response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), status=401, headers={"Content-Type":"application/json"})
    
    # データの整形を開始
    try:
        body = {}
        data : models.USERData = user_data[1]
        
        body["todaySteps"] = data.todaySteps
        body["totalSteps"] = data.totalSteps
        body["ltdReliefDate"] = data.ltdReliefDate
        body["lastInterfereDate"] = data.lastInterfereDate
        body["totalReliefTimes"] = data.totalReliefTimes
        body["currentSeassonReliefTimes"] = data.currentSeasonReliefTimes
        body["lastReliefTimesUpdate"] = data.lastReliefTimesUpdate
        body["property"] = data.property
        body["destructionRate"] = data.destructionRate
        body["civilizationRate"] = data.civilizationRate
        body["currentDebuff"] = data.currentDebuff
        
        ## ownedItemsを整形
        tmp : dict = json.loads(data.ownedItems)
        tmp_keys = tmp.keys()
        ownedItems = []
        
        for id in tmp_keys:
            ownedItems.append({"id":int(id), "count":tmp[id]})
            
        body["ownedItems"] = ownedItems
        
        ## unlockedAchievementを整形
        tmp : dict = json.loads(data.unlockedAchievement)
        tmp_keys = tmp.keys()
        
        unlockedAchievement = []
        
        for id in tmp_keys:
            unlockedAchievement.append({"id":int(id), "status":tmp[id]["status"]})
            
        body["unlockedAchievement"] = unlockedAchievement
        
    except Exception as e:
        logger.debug(f"データの整形過程でエラーが発生しました : {e}")
        return Response(response=json.dumps(Status.get_404(acceptedTime=acceptedTime)), status=404, headers={"Content-Type":"application/json"})
    
    # データの返却を行う
    
    return Response(response=json.dumps(
                        Status.get_200(
                            acceptedTime=acceptedTime, 
                            body=body
                            )
                        ), 
                    status=200, 
                    headers={"Content-Type":"application/json"}
                    )

@FetchUserData.route("/<input_userID>", methods=["put"])
def put_FetchUserData(input_userID):
    
    return ""