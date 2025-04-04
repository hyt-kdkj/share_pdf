from pathlib import Path  
from app import app
import json


class Category:
    def __init__(self, category_name:str):
        self.name = category_name
        category_path = Path(app.config['UPLOAD_FOLDER']) / category_name
        registerd_file = category_path / 'registered.json'

        if not category_path.exists():
            return 'Category not found', 404  # カテゴリフォルダが存在しない場合は404を返す

        # 登録されている論文情報の読み込み
        if not registerd_file.exists():
            papers = []
        else:
            with open(registerd_file, 'r', encoding='utf-8') as file:
                papers = json.load(file)
        self.papers = papers

    def __repr__(self):
        return f'<Category {self.name}>'

    def render_papers_html(self):
        """論文一覧をHTMLとして返す"""
        html = ""
        for paper in self.papers:
            authors = ", ".join(paper.get("authors", []))
            html += f"""
            <li>
                <strong>{paper.get('title', 'Unknown')}</strong> by {authors} ({paper.get('published_date', 'Unknown')})
                <a href="/download/{self.name}/{paper.get('filename', '')}" download>PDFをダウンロード</a>
            </li>
            """
        return html


