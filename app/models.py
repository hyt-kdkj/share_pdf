from pathlib import Path  
from app import app
import json


class Category:

    def __init__(self, category_name:str):
        self.name = category_name
        category_path = Path(app.config['UPLOAD_FOLDER']) / category_name
        self.paper = []
        try:
            with open(category_path / 'registerd.json','r',encoding='utf-8') as file:
                data = json.load(file)
            for d in data:
                self.paper.append(Paper(d))
        except FileNotFoundError:
            # registerd.jsonが存在しない場合は空のリストを使用
            self.paper = []

    def __repr__(self):
        return f'<Category {self.name}>'


class Paper():
    def __init__(self, data:json):
        self.title = data['title']
        self.authors = data['authors']
        self.published_date = data['published_date']
        self.doi = data['DOI']

