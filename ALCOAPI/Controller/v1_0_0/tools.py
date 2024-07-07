# 標準モジュール
import json
import hashlib
import random
import string


# 自作モジュール

def ReadJson(path):
    with open(path, mode = "r") as f:
        response = json.load(f)
        
    return response

def HashText(*text):
    # 文字列結合
    joinedText = "".join(text).encode('utf-8')
    
    # ハッシュ化
    hashedText = hashlib.sha256(joinedText)
    
    # 16進数化したものを返却
    return hashedText.hexdigest()

def CreateUUID(num = 8):
    x = lambda: string.hexdigits[random.randint(0, 15)]
    h = lambda: "".join([x() for _ in range(0, num)])
    
    return h()
    
