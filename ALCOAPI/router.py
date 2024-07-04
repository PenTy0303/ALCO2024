# 標準モジュール
from flask import Flask

# 自作モジュール（相対実行ファイルであるServerから見た相対インポートであることに注意）
from ALCOAPI.API.AuthUser import AuthUser

app = Flask(__name__)
app.config.from_object('ALCOAPI.config')

# BluePrintへ登録
app.register_blueprint(AuthUser) # ユーザー認証機能
