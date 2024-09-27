# 標準モジュール
from flask import Blueprint, request, Response
import json
from jsonschema import validate, ValidationError
from logging import getLogger
import os
import time

# 自作モジュール
from ..DB.CreateEngine import CreateEngine
from ..DB.makeSession import MakeSession
from ..DB.models import USER, USERData, USERSession

from .CreateHistory import CreateHistory
from .tools import ReadJson, HashText ,CreateUserID,ResetEarthStatus


# Blueprint登録
CreateUser = Blueprint("CreateUser", __name__, url_prefix="/CreateUser")

# loggerの取得
logger = getLogger("MainLog").getChild("CreateUser")

# DBエンジンの作成

CE = CreateEngine()

# グローバル変数の宣言
PATH_JSONSCHEMA = "ALCOAPI/" + "v2_0_0" + "/Controller/schema/CreateUser.json"
PAPPER = "TBLJNPUPUFUTVEBF"

@CreateUser.route("", methods=["POST"])
def PostCreateUser():
    
    # アクセス履歴を登録
    CreateHistory(REQUEST=request, method="POST", type="PostCreateUser")
    
    response = {}
    
    # 必要な形式以外を弾く
    
    # Content-Type:application/json以外を弾く
    
    try:
        request.headers["Content-Type"]
    except KeyError as e:
        logger.debug(f"requestHeaderにContent-Typeを含みません : {e}")
        
        response["message"] = "Not found Content-Type"
        return Response(response=json.dumps(response), status=401)
    
    if(request.headers["Content-Type"] == "application/json"):
        
        # 形式が求めるものにあっているかをチェックする
        try:
            # そもそもJSONSCHEMAは存在するか
            try:
                json_schema = ReadJson(PATH_JSONSCHEMA)
            except FileNotFoundError as e:
                logger.error(f"CreateUser用JSONSCHEMAが見つかりません : {e}")
                
                response["message"] = "InternalserverError"
                return Response(response=json.dumps(response), status=500)
            
            validate(request.json, json_schema)
        
        except ValidationError as e:
            logger.debug(f"requestBodyの形式が一致しません : {e}")
                
            response["message"] = "Not Verified request form"
            return Response(response=json.dumps(response), status=401)
    else:
        logger.debug(f"Content-Typeが異なります")
                
        response["message"] = "Not apply Content-Type"
        return Response(response=json.dumps(response), status=401)
    
    # リクエストボディの形式が一致したため，具体的な処理に移る
    
    # セッションを作成
    try:
        session = MakeSession(CE).getSession()
    except Exception as e:
        logger.debug(f"セッション作成エラーです {e}")
        return Response(response=json.dumps(response), status=401)
        
    # プロパティの取得
    content = request.json
    input_name = content["name"]
    input_password = content["pass"]
    
    # テーブルへアクセス
    user = USER()
    userRecord = session.query(USER).filter(USER.name == input_name).all()
    
    # レコード数をチェックし，0なら登録可能
    if(len(userRecord) == 0):
        
        # USERIDを発行
        tmp = CreateUserID(session, USER, USERData)
        userID = tmp["userID"]
        userDataID = tmp["userDataID"]
        
        # パスワードをハッシュ化する
        salt = "alco"
        hashed_input_password = HashText(input_password, salt, PAPPER)
        
        # 発行したものを登録する
        user = USER()
        user.userID = userID
        user.auth = "normalUser"
        user.name = input_name
        user.password = hashed_input_password
        user.salt = salt
        user.userDataID = userDataID
        
        userData = USERData()
        userData.userDataID = userDataID
        userData.todaySteps = 0
        userData.totalSteps = 0
        userData.ltdReliefDate = 0
        userData.lastInterfereDate = 0
        userData.totalReliefTimes = 0
        userData.currentSeasonReliefTimes = 0
        userData.lastReliefTimesUpdate = 0
        userData.property = 0
        userData.destructionRate = 0
        userData.civilizationRate = 0
        userData.currentDebuff = 0
        userData.ownedItems = json.dumps({})
        userData.unlockedAchievement = json.dumps({})
        userData.lastUpdate = time.time()
        
        # 外部キー制約があるのでuserを先にflushへステージ
        session.add(user)
        session.add(userData)
        
        session.commit() 
        
        try:
            ResetEarthStatus(session=session, USERData=USERData, userID=userID)
        except Exception as e:
            logger.debug(f"初期化処理中にエラーが発生しました : {e}")
            session.rollback()
            session.close()
            return Response(response=json.dumps(response), status=401)

        session.close()
        
        
        
        # レスポンス内容を登録する
        response["name"] = input_name
        response["userID"] = userID
        
        return Response(response=json.dumps(response), status=200)

        
    else:
        logger.debug(f"nameが重複しています {input_name}")
        
        response["message"] = "Duplicate Name"
        return Response(response=json.dumps(response), status=401)