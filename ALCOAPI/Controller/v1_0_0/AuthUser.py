# 標準モジュール
from flask import Blueprint, request, Response
import json
from jsonschema import validate, ValidationError
from logging import getLogger

# 自作モジュール
from ALCOAPI.DB.makeSession import MakeSession
from ALCOAPI.DB.models import USER, USERData, USERSession, CLIENTHistory



# 機能分割用のBluePrint登録
# UrlPrefixは仕様書に基づく
AuthUser = Blueprint("AuthUser", __name__, url_prefix = "/ALCOAPI/v1.0.0/AuthUser")

# loggingに登録してあるALCOAPI用のハンドラを取得
logger = getLogger("MainLog").getChild("AuthUser")

# method

PATH_JSONSCHEMA = "ALCOAPI/Controller/v1_0_0/schema/AuthUser.json"

def _ReadJson(path):
    with open(path, mode = "r") as f:
        response = json.load(f)
        
    return response

# router
@AuthUser.route("", methods=['POST'])
def GetAuthUser():
    
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
                json_schema = _ReadJson(PATH_JSONSCHEMA)
            except FileNotFoundError as e:
                logger.error(f"AuthUser用JSONSCHEMAが見つかりません : {e}")
                
                return Response(response=json.dumps(''), status=401)
            
            validate(request.get_json(), json_schema)
        
        except ValidationError as e:
            logger.error(f"requestBodyの形式が一致しません : {e}")
                
            return Response(response=json.dumps(''), status=401)
    else:
        logger.error(f"Content-Typeが異なります")
                
        return Response(response=json.dumps(''), status=401)
    
    # JSONSCEMAにあったリクエストが送られてきたため，具体的な処理に移る
    
    # データベースに接続
    # MakeSession()ハンドリング
    
    
    
        
    