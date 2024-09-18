# normal module
from flask import flask, Blueprint, request
from logging import getLogger
import json
import datetime
import time
import re
import os


# my module
from ..DB import CreateEngine, makeSession, models
from .CreateHistory import CreateHistory as CH
from .Responses import Responses
from .tools import ValidateSessionID


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
PATH_SCHEMA = {"post":f"ALCOAPI/{VERSION}/Controller/schema/FetchItem_post.json", 
               "put": f"ALCOAPI/{VERSION}/Controller/schema/FetchItem_post.json",
               }

## レスポンスクラスの取得
Status = Responses()


# route
@FetchItem.route("/<input_userID>", methods=["post"])
def post_FetchItem(input_userID):
    
    return 

@FetchItem.route("/<input_userID>", methods=["put"])
def put_FetchITem(input_userID):
    
    return


