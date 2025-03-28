from flask import request, render_template
import os  
from app import app
from app.models import Category
import json

@app.route('/')
def index():
    # カテゴリ情報を読み込み
    with open(app.config['CATEGORY_INFO'], 'r', encoding='utf-8') as f:
        data = json.load(f)
    categories = data.get('categories', [])  # 修正: categories配列を取得
    return render_template('index.html', categories=categories)

@app.route('/category_page/<string:category_name>')
def category_page(category_name):
    # カテゴリ名を使用してCategoryインスタンスを作成
    with open(app.config['CATEGORY_INFO'], 'r', encoding='utf-8') as f:
        data = json.load(f)
    if category_name not in data['categories']:
        return 'Category not found', 404  # カテゴリが存在しない場合は404を返す
    category = Category(category_name)  # Categoryクラスを直接使用
    return render_template('category.html', category=category)

@app.route('/upload_pdf', methods=['POST'])
def upload():
    f = request.files.get('file')
    if f and f.filename.endswith('.pdf'):  # PDFファイルのみ許可
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(save_path)
        return '', 204  # 成功時は空のレスポンスを返す
    return 'Invalid file type', 400  # エラー時は400を返す

@app.route('/add_category', methods=['POST'])
def add_category():
    category_name = request.json.get('category_name') #
    if category_name:
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], category_name), exist_ok=True)
        with open(app.config['CATEGORY_INFO'],'r',encoding='utf-8') as file:
            data = json.load(file)
        data['count'] += 1
        data['categories'].append(category_name)  # 修正: categories配列に追加
        with open(app.config['CATEGORY_INFO'],'w',encoding='utf-8') as file:
            json.dump(data,file,ensure_ascii=False,indent=4)
        return '', 204  # 成功時は空のレスポンスを返す
    return 'Category name is required', 400  # エラー時は400を返す

@app.route('/delete_category', methods=['DELETE'])
def delete_dir():
    category_name = request.json.get('category_name')
    if category_name:
        category_path = os.path.join(app.config['UPLOAD_FOLDER'], category_name)
        if os.path.exists(category_path):
            os.rmdir(category_path)
            with open(app.config['CATEGORY_INFO'], 'r', encoding='utf-8') as file:
                data = json.load(file)
            data.pop(category_name, None)  # 修正: discardをpopに変更
            with open(app.config['CATEGORY_INFO'], 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return '', 204
        return 'Category not found', 404
    return 'Category name is required', 400

@app.route('/rename_category', methods=['PUT'])
def rename_category():
    data = request.json
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    if old_name and new_name:
        old_path = os.path.join(app.config['UPLOAD_FOLDER'], old_name)
        new_path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            with open(app.config['CATEGORY_INFO'], 'r', encoding='utf-8') as file:
                data = json.load(file)
            data[new_name] = data.pop(old_name, None)  # 修正: discardをpopに変更
            with open(app.config['CATEGORY_INFO'], 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return '', 204
        return 'Category not found', 404
    return 'Old and new category names are required', 400

