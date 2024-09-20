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
FetchAchievement = Blueprint("FetchAchievement", __name__, url_prefix="/ALCOAPI/v2.0.0/FetchAchievement")

## データベースエンジンクラスの作成
CE = CreateEngine.CreateEngine()

## ロガーの取得
logger = getLogger("MainLog").getChild("FetchAchievement")

## 環境変数の取得
VERSION = os.environ.get("VERSION")

## 正規表現の設定
pattern_userID = r'[a-e0-9]'
matcher_userID = re.compile(pattern_userID)

## JSON用のスキーマのパスを取得
PATH_SCHEMA = f"ALCOAPI/{VERSION}/Controller/schema/FetchAchievement.json"

## レスポンスクラスの取得
Status = Responses()

# route
@FetchAchievement.route("/<input_userID>", methods=["put"])
def put_fetchAchievement(input_userID):
    
    acceptedTime = time.time()
    
    CH(REQUEST=request, method="PUT", type="PUTFetchAchivement")
    
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
        
    ## バリデーション終了
    
    ## 入力されたデータを代入
    input_unlockAchievement = put_data["unlockedAchievement"]
    length = len(input_unlockAchievement)
    
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
        user_data : models.USERData = session\
            .query(models.USER, models.USERData)\
            .join(models.USERData, models.USER.userDataID == models.USERData.userDataID)\
            .filter(models.USER.userID == input_userID)\
            .first()
            
        unlockedAchievements : dict = json.loads(user_data[1].unlockedAchievement)
        
        notUnlockAchievement = []

        ## これまでに解除されたアチーブメント以外であれば解除しない
        for idx in range(length):
            if(str(input_unlockAchievement[idx]["id"]) in unlockedAchievements.keys()):
                unlockedAchievements[str(input_unlockAchievement[idx]["id"])] = {"status":2, "name":input_unlockAchievement[idx]["name"]}
            else:
                notUnlockAchievement.append(idx)
                
        user_data[1].unlockedAchievement = json.dumps(unlockedAchievements, ensure_ascii=False)
        
        session.commit()
        session.close()
            
        if len(notUnlockAchievement) != 0:
            tmp = [input_unlockAchievement[i] for i in notUnlockAchievement]
            logger.debug(f"解除できない実績がありました : {json.dumps(tmp, ensure_ascii=False)}")
            return Response(response=json.dumps(Status.get_200(acceptedTime=acceptedTime, body={"notUnlockAchievement":tmp}), ensure_ascii=False),
                            status=200,
                            headers={"Content-Type":"application/json"}
                            )
            
            
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
