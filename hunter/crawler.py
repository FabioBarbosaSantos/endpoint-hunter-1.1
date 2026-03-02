import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def fetch_html(url):
    r = requests.get(url, timeout=10)
    return r.text

def extract_internal_js(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    base_domain = urlparse(base_url).netloc

    js_files = set()

    for script in soup.find_all("script", src=True):
        src = script["src"]
        full_url = urljoin(base_url, src)
        parsed = urlparse(full_url)

        if parsed.netloc == base_domain:
            js_files.add(full_url)

    return js_files
