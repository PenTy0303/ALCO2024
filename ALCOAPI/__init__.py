# ALCOAPIを読み込むと次のものがパッケージとしてロードされます
import os
print(f"{os.environ.get('VERSION')}がロードされています")
from  .v2_0_0 import router