from ALCOAPI.v1_0_0.router import router
from dotenv import load_dotenv


if __name__ == "__main__":
    # envファイルの読み込み
    load_dotenv()
    router.run()