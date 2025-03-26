from flask import Flask
from flask_dropzone import Dropzone
import os 

app = Flask(__name__)
dropzone = Dropzone(app)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'application/pdf'  # PDFファイルのみ許可
app.config['DROPZONE_MAX_FILE_SIZE'] = 10  # 最大ファイルサイズ（MB）
app.config['DROPZONE_UPLOAD_MULTIPLE'] = False  # 複数ファイルのアップロードを無効化
app.config['DROPZONE_IN_FORM'] = True  # フォーム内で動作するように設定
app.config['DROPZONE_UPLOAD_ACTION'] = 'upload'  # アップロード先のエンドポイント

from app import routes