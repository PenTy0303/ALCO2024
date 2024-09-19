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
router.register_blueprint(ctl.UseSession.UseSession)
router.register_blueprint(ctl.InterfereTime.InterfereTime)
router.register_blueprint(ctl.ReliefTime.ReliefTime)
router.register_blueprint(ctl.FetchItem.FetchItem)
router.register_blueprint(ctl.FetchAchievement.FetchAchievement)
router.register_blueprint(ctl.FetchUserData.FetchUserData)
router.register_blueprint(ctl.GetUserRanking.GetUserRanking)


# method

# ログ取得のためのオブジェクト生成
# 標準Handlerを全て無効化
router.logger.disabled = True
# logging.getLogger("werkzeug").disabled = True

# setLogger実行
SetLogger()



