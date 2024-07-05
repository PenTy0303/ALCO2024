# 標準モジュール
from flask import Blueprint, request
import json

# 機能分割用のBluePrint登録
# UrlPrefixは仕様書に基づく
AuthUser = Blueprint("AuthUser", __name__, url_prefix = "/v1.0.0/AuthUser")

# method

@AuthUser.route("/",methods=['GET'])
def GetAuthUser():
    request = request.get_json()
    