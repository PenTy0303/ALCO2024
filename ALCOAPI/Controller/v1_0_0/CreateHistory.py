# 標準モジュール
from flask import Flask, request
import json
from logging import getLogger

# 自作モジュール
from ALCOAPI.DB.CreateEngine import CreateEngine
from ALCOAPI.DB.makeSession import MakeSession
from ALCOAPI.DB.models import CLIENTHistory

# logger作成
logger = getLogger("MainLog").getChild("CreateHistory")

# エンジンの作成
CE = CreateEngine()

# アクセス履歴保存method
def CreateHistory(REQUEST, METHOD):
    try:
        session = MakeSession(CE).getSession()
        CH = CLIENTHistory()
    except Exception as e:
        logger.error(f"セッション作成エラーです : {e}")
        
        return
        
    # そのリクエストの種別はなにか
