# 標準モジュール
from flask import Blueprint, request, Response
import json
from jsonschema import validate, ValidationError
from logging import getLogger
import os

# 自作モジュール
from ..DB.CreateEngine import CreateEngine
from ..DB.makeSession import MakeSession
from ..DB.models import USER, USERSession

from .CreateHistory import CreateHistory
from .tools import ReadJson, HashText, GetSessionID, VerifyString


# 機能分割用のBluePrint登録
# UrlPrefixは仕様書に基づく
AuthUser = Blueprint("AuthUser", __name__, url_prefix = "/ALCOAPI/v2.0.0/AuthUser")

# loggingに登録してあるALCOAPI用のハンドラを取得
logger = getLogger("MainLog").getChild("AuthUser")

# エンジンの作成
CE = CreateEngine()

# method

PATH_JSONSCHEMA = "ALCOAPI/" + os.environ.get("VERSION") + "/Controller/schema/AuthUser.json"
PAPPER = os.environ["PAPPER"]

# router
@AuthUser.route("", methods=['POST'])
def PostAuthUser():
    
    CreateHistory(REQUEST=request, method="POST",type="PostAuthUser")
    
    response = {}

    # Content-Type = application/json以外を弾く
    
    # まず，Content−Typeを含むかどうかをチェックする
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
                logger.error(f"AuthUser用JSONSCHEMAが見つかりません : {e}")
                
                return Response(response=json.dumps(''), status=500)
            
            validate(request.json, json_schema)
        
        except ValidationError as e:
            logger.debug(f"requestBodyの形式が一致しません : {e}")
                
            return Response(response=json.dumps(''), status=401)
    else:
        logger.debug(f"Content-Typeが異なります")
                
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
    
    # 取得レコード数が０であればuserID不正として処理
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
        if(not VerifyString(hashed_input_passowrd, password)):
            logger.debug(f"userIDに対するパスワードが不正です : {input_userID} {hashed_input_passowrd}")
        
            return Response(response=json.dumps(''), status=401)
    
    # パスワードによる認証が成功したため，セッションIDの発行に移る
    
    # uuidとしてsessionIDを発行する(DBへの登録まで)
    sessionID = GetSessionID(session, USERSession, userID)
    
    response["sessionID"] = sessionID
    
    return Response(response=json.dumps(response), headers={"Content-Type":"application/json"}, status=200)