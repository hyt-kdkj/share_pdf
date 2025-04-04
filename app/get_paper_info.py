import doi
import subprocess
import requests
import json
import tempfile  # 一時ファイルを作成するためにtempfileをインポート
import re  # 修正: 正規表現を使用するためにインポート

def get_paper_metadata(doi):
    """DOIから論文情報を取得"""
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        title = data["message"].get("title", ["Unknown"])[0]
        authors = [author["given"] + " " + author["family"] for author in data["message"].get("author", [])]
        published = data["message"].get("published-print", {}).get("date-parts", [["Unknown"]])[0]
        return title, authors, "-".join(map(str, published))
    return None, None, None  # 情報が取得できなかった場合

# def extract_metadata_from_pdf(pdf_file):
#     """PDFファイルからDOIを取得し、論文情報を返す"""
#     # 一時ファイルにPDFを保存
#     with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as temp_pdf:
#         pdf_file.seek(0)  # ファイルポインタを先頭に戻す
#         temp_pdf.write(pdf_file.read())
#         temp_pdf.flush()  # データをディスクに書き込む

#         # 一時ファイルのパスをdoi.pdf_to_doiに渡す
#         DOI = doi.pdf_to_doi(temp_pdf.name)
#         if DOI:
#             match = re.search(r'10\.\d{4,9}/[\w\-._;()/:]+', DOI, re.IGNORECASE)

#             if match:
#                 DOI = match.group(0)  # DOIの正しい部分を抽出
#                 # DOI = (DOI.split('/'))[:2].join('/')
#                 title, authors, published_date = get_paper_metadata(DOI)
#                 return json.dumps({
#                     "title": title,
#                     "authors": authors,
#                     "published_date": published_date,
#                     "DOI": DOI
#                 }, indent=4), True
#     return json.dumps({}, indent=4), False

def extract_metadata_from_pdf(pdf_file):
    """PDFファイルからDOIを取得し、論文情報を返す"""
    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as temp_pdf:
        pdf_file.seek(0)
        temp_pdf.write(pdf_file.read())
        temp_pdf.flush()
        
        try:
            # pdf2doi を用いて DOI を取得
            result = subprocess.run(["pdf2doi", temp_pdf.name], capture_output=True, text=True)
            doi_match = re.search(r'10\.\d{4,9}/[\w\-._;()/:]+', result.stdout, re.IGNORECASE)
            
            if doi_match:
                doi = doi_match.group(0)
                title, authors, published_date = get_paper_metadata(doi)
                return json.dumps({
                    "title": title,
                    "authors": authors,
                    "published_date": published_date,
                    "DOI": doi
                }, indent=4), True
        except Exception as e:
            print(f"Error extracting DOI: {e}")
    
    return json.dumps({}, indent=4), False