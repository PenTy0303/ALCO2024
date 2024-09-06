import ALCOAPI
from dotenv import load_dotenv


if __name__ == "__main__":
    # envファイルの読み込み
    load_dotenv()
    ALCOAPI.router.router.run()