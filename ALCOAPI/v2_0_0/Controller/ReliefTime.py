from flask import Blueprint, request, Response
from logging import getLogger
import re
import os
import json
import time

# 自作モジュール
from ..DB import CreateEngine, makeSession, models
from .CreateHistory import CreateHistory as CH
from .Responses import Responses
from .tools import ValidateSessionID

# BluePrintの登録
ReliefTime = Blueprint("ReliefTime", __name__,  url_prefix="/ALCOAPI/v2.0.0/ReliefTime")

# データベースのエンジン作成
CE = CreateEngine.CreateEngine()

# 環境変数の登録
VERSION = os.environ.get("VERSION")

# loggerの取得
logger = getLogger("MainLog").getChild("ReliefTime")

# 正規表現の登録
pattern_userID = r'[a-z0-9]'
matcher_userID = re.compile(pattern_userID)

# レスポンスクラスの登録

Status = Responses()