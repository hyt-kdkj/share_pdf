from flask import request, render_template, redirect, url_for, jsonify, send_file
from pathlib import Path  # 修正: pathlibをインポート
from app import app
from app.models import Category
import json
from urllib.parse import unquote
from app.get_paper_info import extract_metadata_from_pdf
from werkzeug.utils import secure_filename  # 修正: ファイル名の安全性を確保するためにインポート
<<<<<<< HEAD

=======
>>>>>>> sub-working-tree


@app.route('/')
def index():
    # カテゴリ情報を読み込み
    with open(app.config['CATEGORY_LIST'], 'r', encoding='utf-8') as f:
        data = json.load(f)
    categories = data.get('categories', []) 
    return render_template('index.html', categories=categories)

@app.route('/category_page/<string:category_name>')
def category_page(category_name):
    if check_category_existence(category_name):
        category = Category(category_name)
        return render_template('category.html', category=category)
    else:
        with open(app.config['CATEGORY_LIST'], 'r', encoding='utf-8') as f:
            categories = json.load(f)
        categories['categories'].remove(category_name)
        with open(app.config['CATEGORY_LIST'], 'w', encoding='utf-8') as file:
            json.dump(categories, file, ensure_ascii=False, indent=4)
        return redirect(url_for('index'),categories=categories)

<<<<<<< HEAD
    category = Category(category_name)
    return render_template('category.html', category=category)
=======
>>>>>>> sub-working-tree

@app.route('/upload/<string:category_name>', methods=['POST'])
def upload(category_name):
    f = request.files.get('file')
    if not f:
        return 'No file provided', 400  # ファイルが提供されていない場合のエラーハンドリング

    # メタデータを取得
    new_paper, flag = extract_metadata_from_pdf(f)

    if flag and f.filename.endswith('.pdf'):  # PDFファイルのみ許可
        category_path = Path(app.config['UPLOAD_FOLDER']) / category_name
        category_path.mkdir(parents=True, exist_ok=True)  # カテゴリフォルダを作成

        # ファイル名を安全にし、重複を防ぐ
        original_filename = secure_filename(f.filename)
        save_path = category_path / original_filename

        # ファイル名の重複をチェック
        if save_path.exists():
            return 'File with the same name already exists', 400  # 修正: JSONレスポンスを文字列に変更

        try:
            # ファイルを保存
            f.seek(0)  # ファイルポインタを先頭に戻す
            f.save(save_path)

            # registerd.jsonを更新
            registerd_file = category_path / 'registerd.json'
            if registerd_file.exists():
                with open(registerd_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            else:
                data = []

            # 新しい論文情報を追加
            new_paper_data = json.loads(new_paper)  # JSON文字列を辞書に変換
            new_paper_data["filename"] = save_path.name  # ファイル名を追加
            data.append(new_paper_data)

            with open(registerd_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            # リダイレクトして画面をリロード
            return redirect(url_for('category_page', category_name=category_name))
        except Exception as e:
            return f"Error: {str(e)}", 500  
    return 'Invalid file type', 400  

@app.route('/add_category', methods=['POST'])
def add_category():
    category_name = request.json.get('category_name')
    if category_name:
        #新しいカテゴリーディレクトリを追加
        category_path = Path(app.config['UPLOAD_FOLDER']) / category_name
        category_path.mkdir(parents=True, exist_ok=True)

        #カテゴリーディレクトリ内に登録された論文情報を管理するためのjsonファイルを追加
        json_file = category_path / "registerd.json"
        json_file.write_text(json.dumps([]), encoding="utf-8")

        with open(app.config['CATEGORY_LIST'], 'r', encoding='utf-8') as file:
            data = json.load(file)

        if category_name not in data['categories']:
            data['categories'].append(category_name)  
            data['categories'].sort()
            with open(app.config['CATEGORY_LIST'], 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        return 'Category added successfully', 200  
    return 'Category name is required', 400  

@app.route('/delete_category', methods=['DELETE'])
def delete_category():
    category_name = request.json.get('category_name')
    if category_name:
        category_path = Path(app.config['UPLOAD_FOLDER']) / category_name
        if category_path.exists():
            # ディレクトリ内のファイルを確認
            files = list(category_path.iterdir())
            if len(files) == 1 and files[0].name == "registerd.json":
                files[0].unlink()  # registerd.json を削除
                category_path.rmdir()  # カテゴリフォルダ自体を削除

                # CATEGORY_LISTからカテゴリを削除
                with open(app.config['CATEGORY_LIST'], 'r', encoding='utf-8') as file:
                    data = json.load(file)
                if isinstance(data.get('categories'), list) and category_name in data['categories']:
                    data['categories'].remove(category_name)
                    with open(app.config['CATEGORY_LIST'], 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

                return 'Category deleted successfully', 200  
            return "Category must contain only 'registerd.json' to be deleted", 400  
        return 'Category not found', 404  
    return 'Category name is required', 400  #

@app.route('/rename_category', methods=['PUT'])
def rename_category():
    data = request.json
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    if old_name and new_name:
        old_path = Path(app.config['UPLOAD_FOLDER']) / old_name
        new_path = Path(app.config['UPLOAD_FOLDER']) / new_name
        if old_path.exists() and not new_path.exists():
            old_path.rename(new_path)
            with open(app.config['CATEGORY_LIST'], 'r', encoding='utf-8') as file:
                data = json.load(file)
            if isinstance(data.get('categories'), list) and old_name in data['categories']:
                data['categories'].remove(old_name)  
                data['categories'].append(new_name)  
                data['categories'].sort()
                with open(app.config['CATEGORY_LIST'], 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
            return 'Category renamed successfully', 200  
        return 'Category not found', 404  
    return 'Old and new category names are required', 400  

@app.route('/download/<string:category_name>/<string:filename>')
def download_paper(category_name, filename):
    # 受け取ったファイル名をデコード
    filename = unquote(filename)

    file_path = Path(app.config['UPLOAD_FOLDER']) / category_name / filename

    if file_path.exists():
        return send_file(file_path, as_attachment=True, download_name=filename)
    else:
<<<<<<< HEAD
        return 'File not found', 404
=======
        return 'File not found', 404  
>>>>>>> sub-working-tree

def serve_pdf():
    # PDFファイルのパスを指定
    filepath = Path(app.config['UPLOAD_FOLDER']) / 'ppp.pdf'
    if filepath.exists():
        return send_file(filepath, as_attachment=True, download_name='ppp.pdf')
<<<<<<< HEAD
    return 'File not found', 404 
=======
    return 'File not found', 404  

def check_category_existence(category_name):
    category_path = Path(app.config['UPLOAD_FOLDER']) / category_name
    return category_path.exists()

>>>>>>> sub-working-tree

if __name__ == '__main__':
    app.run(debug=True)
