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
from ALCOAPI.Controller.v1_0_0.tools import ReadJson, HashText ,CreateUserID


# Blueprint登録
CreateUser = Blueprint("CreateUser", __name__, url_prefix="/ALCOAPI/v1.0.0/CreateUser")

# loggerの取得
logger = getLogger("MainLog").getChild("CreateUser")

# DBエンジンの作成

CE = CreateEngine()

# グローバル変数の宣言
PATH_JSONSCHEMA = "ALCOAPI/Controller/v1_0_0/schema/CreateUser.json"
PAPPER = os.environ["PAPPER"]

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
                
        return Response(response=json.dumps(''), status=401)
    
    if(request.headers["Content-Type"] == "application/json"):
        
        # 形式が求めるものにあっているかをチェックする
        try:
            # そもそもJSONSCHEMAは存在するか
            try:
                json_schema = ReadJson(PATH_JSONSCHEMA)
            except FileNotFoundError as e:
                logger.error(f"CreateUser用JSONSCHEMAが見つかりません : {e}")
                
                return Response(response=json.dumps(''), status=401)
            
            validate(request.json, json_schema)
        
        except ValidationError as e:
            logger.debug(f"requestBodyの形式が一致しません : {e}")
                
            return Response(response=json.dumps(''), status=401)
    else:
        logger.debug(f"Content-Typeが異なります")
                
        return Response(response=json.dumps(''), status=401)
    
    # リクエストボディの形式が一致したため，具体的な処理に移る
    
    # セッションを作成
    try:
        session = MakeSession(CE).getSession()
    except Exception as e:
        logger.debug(f"セッション作成エラーです {e}")
        
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
        userData.point = 0
        userData.favorableRate = 0
        userData.reloadedDate = datetime.datetime.now()
        userData.weekSteps = json.dumps({"01":0, "02":0, "03":0, "04":0, "05":0, "06":0, "07":0})
        
        # 外部キー制約があるのでuserを先にflushへステージ
        session.add(user)
        session.flush()
        session.add(userData)
        
        session.commit()
        
        session.close()
        
        # レスポンス内容を登録する
        response["name"] = input_name
        response["userID"] = userID
        
        return Response(response=json.dumps(response), status=200)
        
        
        
    else:
        logger.debug(f"nameが重複しています {input_name}")
        
        return Response(response=json.dumps(''), status=401)
    
    
    

    
    