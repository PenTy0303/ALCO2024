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
FetchEarthRelief = Blueprint("FetchEarthRelief", __name__, url_prefix="/ALCOAPI/v2.0.0/FetchEarthRelief")

## get env
VERSION = os.environ.get("VERSION")

## create db engine
CE = CreateEngine.CreateEngine()

## get logger
logger = getLogger("MainLog").getChild("FetchEarthRelief")

## register re matcher
pattern_userID = r'[a-e0-9]'
matcher_userID = re.compile(pattern_userID)

## json schema path
PATH_SCHEMA = f"ALCOAPI/{VERSION}/Controller/schema/FetchEarthRelief_post.json"

## instance Resposnses
Status = Responses()

@FetchEarthRelief.route("/<input_userID>", methods=["post"])
def post_FetchEarthRelief(input_userID):
    acceptedTime = time.time()
    
    CH(REQUEST=request, method="POST", type="PostFetchiItem")
    
    # 入力データのバリデーション
    if(not matcher_userID.match(input_userID)):
        logger.debug("userIDが不正です")
        return Response(
            response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), 
            status=401, 
            headers={"Content-Type":"application/json"}
            ) 
    
    ## sessionIDの存在チェック
    try:
        input_sessionID = request.args.get("sessionID")
    except KeyError as e:
        logger.debug(f"sessionIDが見つかりません:{e}")
        return Response(
            response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), 
            status=401, 
            headers={"Content-Type":"application/json"}
            ) 
        
    ## sessionIDのバリデーション
    if(not matcher_userID.match(input_sessionID)):
        logger.debug("sesionIDが不正です　")
        return Response(
            response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), 
            status=401, 
            headers={"Content-Type":"application/json"}
            )
        
    ## DBへの接続
    try:
        session = makeSession.MakeSession(CE=CE).getSession()
    except Exception as e:
        logger.debug(f"データベースへの接続に失敗しました : {e}")
        return Response(
            response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), 
            status=401, 
            headers={"Content-Type":"application/json"}
            )
    
    ## sessionIDの有効性チェック
    if(not ValidateSessionID(session=session, USERSession=models.USERSession, sessionID=input_sessionID, userID=input_userID)):
        # 認証が通らなかった場合はそのままレスポンスする
        logger.debug("セッションの認証が通りませんでした")
        session.close()
        return Response(
            response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), 
            status=401, 
            headers={"Content-Type":"application/json"}
            )
        
    session.close()
    ## 入力されたJSONデータのバリデーション
    
    ### ContentType;application/jsonの存在確認
    try:
        if(not request.headers["Content-Type"] == "application/json"):
            logger.debug("リクエストデータが不正です")
            return Response(
                response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), 
                status=401, 
                headers={"Content-Type":"application/json"}
                )
        else:
            ### 中身をJSONにダンプできるかどうかの確認  
            try:
                post_data = request.json
            except Exception as e:
                logger.debug("リクエストデータをJSONへパースできません")
                return Response(
                    response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), 
                    status=401, 
                    headers={"Content-Type":"application/json"}
                    )
            
            ### 中身がJSONスキーマにあっているかチェック
            #### JSONスキーマの読み込み
            try:
                json_schema = ReadJson(PATH_SCHEMA)
                
            except FileNotFoundError as e:
                logger.debug(f"JSON_SCHEMAファイルが見つかりませんでした : {e}")
                return Response(
                    response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), 
                    status=401, 
                    headers={"Content-Type":"application/json"}
                    )
                
            except Exception as e:
                logger.debug(f"スキーマ読み込みにつき予期せぬエラーが発生しました : {e}")
                return Response(
                    response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), 
                    status=401, 
                    headers={"Content-Type":"application/json"}
                    )
            
            ### JSONスキーマのチェック
            try:
                validate(post_data, json_schema)
            except ValidationError as e:
                logger.debug(f"ValidationErrorが発生しました : {e}")
                return Response(
                    response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), 
                    status=401, 
                    headers={"Content-Type":"application/json"}
                    )
    except KeyError as e:
        logger.debug(f"Content-Typeを持っていません : {e}")
        return Response(
                    response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), 
                    status=401, 
                    headers={"Content-Type":"application/json"}
                    )
        
    except Exception as e:
        logger.debug("バリデーションの過程で異常終了しました : {e}")
        return Response(
                    response=json.dumps(Status.get_404(acceptedTime=acceptedTime)), 
                    status=404, 
                    headers={"Content-Type":"application/json"}
                    )
            
    # 入力データのバリデーション終了
    
    # 入力データの代入
    isRelief : int = post_data["isRelief"]
    input_unlockAchievement : list[dict]= post_data["unlockedAchievement"]
    
    
    
    return ""
