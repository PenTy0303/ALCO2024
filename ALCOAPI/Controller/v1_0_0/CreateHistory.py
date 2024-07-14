# 標準モジュール
from flask import Flask, request
import json
import datetime
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
def CreateHistory(REQUEST, method, type, addition=""):
    try:
        session = MakeSession(CE).getSession()
        CH = CLIENTHistory()
    except Exception as e:
        logger.error(f"セッション作成エラーです : {e}")
        
        return False
        
    # bodyにデータが入っているのかqueryにデータが入っているのか
    if(method == "POST"):
        # POST
        payload = json.dumps(REQUEST.get_json())
    else:
        # GET
        tmp = REQUEST.args.to_dict()
        tmp["url"] = addition
        payload = json.dumps(tmp)
        
    # データの登録
    CH.date = datetime.datetime.now()
    CH.type = type
    CH.method = method
    CH.payload = payload
    
    session.add(CH)
    
    session.commit()
    
    session.close()
    
    return True
        
    

    