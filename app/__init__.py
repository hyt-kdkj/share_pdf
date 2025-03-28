import os
from flask import Flask
from flask_dropzone import Dropzone

# Flask アプリのインスタンスを作成
app = Flask(__name__)

# 設定の適用
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # ディレクトリが存在しない場合に作成
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'application/pdf'  # PDFファイルのみ許可
app.config['DROPZONE_MAX_FILE_SIZE'] = 10  # 最大ファイルサイズ（MB）
app.config['DROPZONE_UPLOAD_MULTIPLE'] = False  # 複数ファイルのアップロードを無効化
app.config['DROPZONE_IN_FORM'] = True  # フォーム内で動作するように設定
app.config['DROPZONE_UPLOAD_ACTION'] = 'upload'  # アップロード先のエンドポイント
app.config['CATEGORY_INFO'] = 'app/category.json'  # カテゴリ情報のファイルパス

# 拡張機能の初期化
dropzone = Dropzone(app)

# ルーティングとモデルをインポート
from app import routes, models
