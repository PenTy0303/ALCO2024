# 標準モジュール
from flask import Flask

# 自作モジュール（相対実行ファイルであるServerから見た相対インポートであることに注意）
from ALCOAPI.Controller.v1_0_0.AuthUser import AuthUser
app = Flask(__name__)
app.config.from_object('ALCOAPI.config')

# BluePrintへ登録
app.register_blueprint(AuthUser) # ver1のAPI群の追加
