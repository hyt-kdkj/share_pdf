from flask import request, render_template
import os  
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads', methods=['POST'])
def upload():
    f = request.files.get('file')
    if f and f.filename.endswith('.pdf'):  # PDFファイルのみ許可
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(save_path)
        return '', 204  # 成功時は空のレスポンスを返す
    return 'Invalid file type', 400  # エラー時は400を返す

@app.route('/add_dir') 
def add_dir():
    # ディレクトリを新しく追加する
    filename = 'ppp'
    if not os.path.isdir(filename):
        os.makedirs(filename)
        return 'Directory created successfully', 201  # 成功時のレスポンスを明示
    return 'Directory is already exist.',201

@app.route('delete_dir')
def delete_dir():
    # ディレクトリを削除，ただしディレクトリが空であることを条件とする
    filename = 'ppp'
    if (not os.path.isdir(filename)) and (not os.listdir(filename)):
        os.remove(filename)
        return 'Directory deleted successfully', 201 
    return 'Directory is alreadydeleted', 201

