import ALCOAPI.v2_0_0 as funcs
from dotenv import load_dotenv


if __name__ == "__main__":
    # envファイルの読み込み
    load_dotenv()
    funcs.router.router.run()