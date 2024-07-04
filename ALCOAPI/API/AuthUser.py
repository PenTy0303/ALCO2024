# 標準モジュール
from flask import Blueprint

# 機能分割用のBluePrint登録
# UrlPrefixは仕様書に基づく
AuthUser = Blueprint("AuthUser", __name__, url_prefix = "/AuthUser")

@AuthUser.route("/")
def index():
    return "AuthUserIndex"