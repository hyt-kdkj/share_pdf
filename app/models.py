import json
import os
from app.get_paper_info import extract_metadata_from_pdf
from app import app

class Category:

    def __init__(self, category_name):
        self.name = category_name
        self.read_pdfs()

    def __repr__(self):
        return f'<Category {self.name}>'

    def read_pdfs(self):
        """uploadsフォルダ内のカテゴリフォルダにあるすべてのPDFファイルを読み込み、メタデータを取得"""
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], self.name)  # 修正: カテゴリ名を使用
        self.file_paths = []  # 修正: 初期化を追加
        papers_metadata = []
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.pdf'):
                    file_path = os.path.join(folder_path, file_name)
                    try:
                        title, authors, published_date, doi = extract_metadata_from_pdf(file_path)
                        if title and authors and published_date and doi:
                            papers_metadata.append({
                                "title": title,
                                "authors": authors,
                                "published_date": published_date,
                                "doi": doi,
                                "file_path": file_path
                            })
                            self.file_paths.append(file_path)  # ファイルパスを記録
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
        else:
            print(f"Error: Folder {folder_path} does not exist.")

        self.papers_metadata = papers_metadata  # 修正: タイポ修正

