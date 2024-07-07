from ALCOAPI.router import router
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    # envファイルの読み込み
    load_dotenv()
    router.run()