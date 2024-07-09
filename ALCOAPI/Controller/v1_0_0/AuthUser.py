# 標準モジュール
from flask import Blueprint, request, Response
import json
from jsonschema import validate, ValidationError
from logging import getLogger
import hashlib
import os

# 自作モジュール
from ALCOAPI.DB.CreateEngine import CreateEngine
from ALCOAPI.DB.makeSession import MakeSession
from ALCOAPI.DB.models import USER, USERData, USERSession, CLIENTHistory

from ALCOAPI.Controller.v1_0_0.CreateHistory import CreateHistory
from ALCOAPI.Controller.v1_0_0.tools import ReadJson, HashText, CreateSessionID


# 機能分割用のBluePrint登録
# UrlPrefixは仕様書に基づく
AuthUser = Blueprint("AuthUser", __name__, url_prefix = "/ALCOAPI/v1.0.0/AuthUser")

# loggingに登録してあるALCOAPI用のハンドラを取得
logger = getLogger("MainLog").getChild("AuthUser")

# エンジンの作成
CE = CreateEngine()

# method

PATH_JSONSCHEMA = "ALCOAPI/Controller/v1_0_0/schema/AuthUser.json"
PAPPER = os.environ["PAPPER"]

# router
@AuthUser.route("", methods=['POST'])
def GetAuthUser():
    
    CreateHistory(REQUEST=request, method="POST",type="GetAuthUser")
    
    response = {}

    # Content-Type = application/json以外を弾く
    
    # まず，Content−Typeを含むかどうかをチェックする
    try:
        request.headers["Content-Type"]
    except KeyError as e:
        logger.error(f"requestHeaderにContent-Typeを含みません : {e}")
                
        return Response(response=json.dumps(''), status=401)
    
    if(request.headers["Content-Type"] == "application/json"):
        
        # 形式が求めるものにあっているかをチェックする
        try:
            # そもそもJSONSCHEMAは存在するか
            try:
                json_schema = ReadJson(PATH_JSONSCHEMA)
            except FileNotFoundError as e:
                logger.error(f"AuthUser用JSONSCHEMAが見つかりません : {e}")
                
                return Response(response=json.dumps(''), status=401)
            
            validate(request.json, json_schema)
        
        except ValidationError as e:
            logger.error(f"requestBodyの形式が一致しません : {e}")
                
            return Response(response=json.dumps(''), status=401)
    else:
        logger.error(f"Content-Typeが異なります")
                
        return Response(response=json.dumps(''), status=401)
    
    # JSONSCEMAにあったリクエストが送られてきたため，具体的な処理に移る
    
    # データベースに接続
    # MakeSession()ハンドリング
    
    try:
        session = MakeSession(CE).getSession()
    except Exception as e:
        logger.error("セッション作成エラーです")
        
        return Response(request=json.dumps(""), status=401)
    
    # データベースのモデルにアクセス
    User = USER()
    
    # Requestデータのセット
    contents = request.get_json()
    input_userID = contents["userID"]
    input_password = contents["pass"]
    
    # データベースのデータを確保
    userRecord = session.query(USER).filter(USER.userID == input_userID).all()
    
    # 取得データ数が０であればuserID不正として処理
    if(len(userRecord) == 0):
        logger.debug(f"userIDが不正です : {input_userID}")
        
        return Response(response=json.dumps(''), status=401)
    
    else:
        # 必要データを取っておく
        userID = userRecord[0].userID
        password = userRecord[0].password
        salt = userRecord[0].salt
        
        # 送信されたパスワードをハッシュ化して照合
        # ハッシュ化する
        hashed_input_passowrd = HashText(input_password, salt, PAPPER)
        
        # 照合する
        if(not hashed_input_passowrd == password):
            logger.debug(f"userIDに対するパスワードが不正です : {input_userID} {hashed_input_passowrd}")
            print(password)
        
            return Response(response=json.dumps(''), status=401)
    
    # パスワードによる認証が成功したため，セッションIDの発行に移る
    
    # uuidとしてsessionIDを発行する(DBへの登録まで)
    sessionID = CreateSessionID(session, USERSession, userID)
    
    response["sessionID"] = sessionID
    
    return Response(response=json.dumps(response), status=200)
    
    
    
    
    
        
    