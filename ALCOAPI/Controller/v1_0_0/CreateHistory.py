# 標準モジュール
from flask import Flask, request
import json
from logging import getLogger

# 自作モジュール
from ALCOAPI.DB.makeSession import MakeSession
from ALCOAPI.DB.models import CLIENTHistory

# logger作成
logger = getLogger("MainLog").getChild("CreateHistory")

# デコレータ
def CreateHistory(REQUEST):
    def _decorator(f):
        def _wrapper(*args, **keywords):
            
            try:
                session = MakeSession().getSession()
                CH = CLIENTHistory()
            except Exception as e:
                logger.error(f"セッション作成エラーです : {e}")
                
            CH.
            
            
            
        return _wrapper
    
    return _decorator