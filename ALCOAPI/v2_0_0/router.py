# 標準モジュール
from flask import Flask
import os


# 機能群
from . import Controller as ctl


# method
from .SetLogger import SetLogger

router = Flask(__name__)
router.config.from_object('ALCOAPI.'+os.environ.get("VERSION")+'.config')

# BluePrintへ登録
router.register_blueprint(ctl.AuthUser.AuthUser) 
router.register_blueprint(ctl.CreateUser.CreateUser)


# method

# ログ取得のためのオブジェクト生成
# 標準Handlerを全て無効化
router.logger.disabled = True
# logging.getLogger("werkzeug").disabled = True

# setLogger実行
SetLogger()



