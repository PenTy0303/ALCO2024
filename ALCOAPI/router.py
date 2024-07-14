# 標準モジュール
from flask import Flask

# 自作モジュール（相対実行ファイルであるServerから見た相対インポートであることに注意）
# 機能群
from ALCOAPI.Controller.v1_0_0.AuthUser import AuthUser
from ALCOAPI.Controller.v1_0_0.CreateUser import CreateUser
from ALCOAPI.Controller.v1_0_0.HandleUserData import HandleUserData


# method
import ALCOAPI.setLogger as setLogger

router = Flask(__name__)
router.config.from_object('ALCOAPI.config')

# BluePrintへ登録
router.register_blueprint(AuthUser) # ver1のAPI群の追加
router.register_blueprint(CreateUser)
router.register_blueprint(HandleUserData)


# method

# ログ取得のためのオブジェクト生成
# 標準Handlerを全て無効化
router.logger.disabled = True
# logging.getLogger("werkzeug").disabled = True

# setLogger実行
setLogger.SetLogger()

