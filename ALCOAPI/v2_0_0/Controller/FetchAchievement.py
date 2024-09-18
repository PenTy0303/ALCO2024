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
    
    return
