# normal module
from flask import Blueprint, request, Response
from logging import getLogger
from jsonschema import validate, ValidationError
import json
import datetime
import time
import re
import os


# my module
from ..DB import CreateEngine, makeSession, models
from .CreateHistory import CreateHistory as CH
from .Responses import Responses
from .tools import ReadJson, ValidateSessionID


# initialize
## BluePrintの取得
FetchItem = Blueprint("FetchItem", __name__, url_prefix="/ALCOAPI/v2.0.0/FetchItem")

## データベースエンジンクラスの作成
CE = CreateEngine.CreateEngine()

## ロガーの取得
logger = getLogger("MainLog").getChild("FetchItem")

## 環境変数の取得
VERSION = os.environ.get("VERSION")

## 正規表現の設定
pattern_userID = r'[a-e0-9]'
matcher_userID = re.compile(pattern_userID)

## JSON用のスキーマのパスを取得
PATH_SCHEMA = {
    "post":f"ALCOAPI/{VERSION}/Controller/schema/FetchItem_post.json", 
    "put": f"ALCOAPI/{VERSION}/Controller/schema/FetchItem_put.json",
    }

## レスポンスクラスの取得
Status = Responses()


# route
@FetchItem.route("/<input_userID>", methods=["post"])
def post_FetchItem(input_userID):
    
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
                json_schema = ReadJson(PATH_SCHEMA["post"])
                
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
    itemID = post_data["itemID"]
    itemCount = post_data["itemCount"]
    property = post_data["property"]
    
    # 次にアイテムの購入を行う
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
    
    ## DBへのアイテム登録
    try:
        user_data = session\
            .query(models.USER, models.USERData)\
            .join(models.USERData, models.USER.userDataID == models.USERData.userDataID)\
            .filter(models.USER.userID == input_userID)\
            .first()
        
        user_owned_items = json.loads(user_data[1].ownedItems)
        user_owned_items[str(itemID)] = itemCount
        
        ### データの更新を開始
        user_data[1].ownedItems = json.dumps(user_owned_items)
        user_data[1].property = property
        
        session.commit()
        session.close()
        
        
    except Exception as e:
        
        session.rollback()
        session.close()
        
        logger.debug(f"データベース接続中にエラーが発生しました : {e}")
        return Response(
            response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), 
            status=401, 
            headers={"Content-Type":"application/json"}
            )
        
    # データをレスポンスする
    
    return Response(
            response=json.dumps(Status.get_200(acceptedTime=acceptedTime)), 
            status=200, 
            headers={"Content-Type":"application/json"}
            )
        
@FetchItem.route("/<input_userID>", methods=["put"])
def put_FetchITem(input_userID):
    
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
                put_data = request.json
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
                json_schema = ReadJson(PATH_SCHEMA["put"])
                
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
                validate(put_data, json_schema)
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
    
    # 入力データを代入する
    itemID = put_data["itemID"]
    itemCount = put_data["itemCount"]
    destructionRate = put_data["destructionRate"]
    civilizationRate = put_data["civilizationRate"]
    debuff = put_data["debuff"]
    
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
    
    # DBへデータを更新する
    try:
        user_data = session.query(models.USER, models.USERData).join(models.USERData, models.USERData.userDataID == models.USER.userDataID).filter(models.USER.userID == input_userID).first()
        
        owned_item : dict = json.loads(user_data[1].ownedItems)
        if(str(itemID) in owned_item.keys()):
            owned_item[str(itemID)] = itemCount
            
            ## 実際のデータの更新
            
            user_data[1].ownedItems = json.dumps(owned_item)
            user_data[1].destructionRate = destructionRate
            user_data[1].civilizationRate = civilizationRate
            user_data[1].debuff = debuff
            user_data[1].lastInterfereDate = time.time()
        
        else:
            # まだ所持していないアイテムを使用しようしよとするとエラーが発生する
            raise Exception
        
        session.commit()
        session.close()       
        
    except Exception as e:
        
        session.rollback()
        session.close()
        
        logger.debug(f"DBへの書き込み途中でエラーが発生しました : {e}")
        return Response(
            response=json.dumps(Status.get_401(acceptedTime=acceptedTime)), 
            status=401, 
            headers={"Content-Type":"application/json"}
            )
        
    return Response(
            response=json.dumps(Status.get_200(acceptedTime=acceptedTime)), 
            status=200, 
            headers={"Content-Type":"application/json"}
            )


