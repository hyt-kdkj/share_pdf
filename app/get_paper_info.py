import doi
import requests

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

def extract_metadata_from_pdf(pdf_file):
    """PDFファイルからDOIを取得し、論文情報を返す"""
    DOI = doi.pdf_to_doi(pdf_file)
    if DOI:
        title, authors, published_date = get_paper_metadata(DOI)
        return title, authors, published_date, DOI
    return None, None, None, None  #DOIが取得できなかった場合


if __name__ == "__main__":
    filename = 'ppp.pdf'
    title, authors, published_date, DOI = extract_metadata_from_pdf(filename)
    print('title:',title)
    print('authors:',authors)
    print('published date:',published_date)
    print('doi:',DOI)