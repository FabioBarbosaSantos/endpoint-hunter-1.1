import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from hunter.config import DEFAULT_HEADERS, TIMEOUT
from requests_html import HTMLSession

def fetch_html(url, verbose=False):
    if verbose:
        print(f"[+] Requesting HTML: {url}")
    r = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    return r.text

def extract_html_links(html, base_url, verbose=False):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for tag in soup.find_all(["a", "link"], href=True):
        full_url = urljoin(base_url, tag["href"])
        links.add(full_url)

    for tag in soup.find_all("form", action=True):
        full_url = urljoin(base_url, tag["action"])
        links.add(full_url)

    if verbose:
        print(f"[DEBUG] Found {len(links)} HTML links")
    return list(links)

def extract_scripts(html, base_url, verbose=False):
    soup = BeautifulSoup(html, "html.parser")
    scripts = set()

    for script in soup.find_all("script", src=True):
        full_url = urljoin(base_url, script["src"])
        scripts.add(full_url)
        if verbose:
            print(f"[DEBUG] Found JS: {full_url}")
    return list(scripts)

def fetch_js_files(js_urls, verbose=False):
    contents = []
    for url in js_urls:
        try:
            if verbose:
                print(f"[+] Fetching JS: {url}")
            r = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
            if r.status_code == 200:
                contents.append(r.text)
        except requests.RequestException:
            continue
    return contents

def fetch_dynamic_links(url, verbose=False):
    """
    Captura requisições XHR/Fetch via requests_html (headless, leve)
    """
    if verbose:
        print(f"[+] Launching session to capture XHR/Fetch for {url}")
    session = HTMLSession()
    r = session.get(url)
    r.html.render(timeout=20, sleep=1)  # roda JS leve para popular a página
    dynamic_urls = set()

    for req in r.html.page._responses.values():
        if "http" in req.url:
            dynamic_urls.add(req.url)
    
    if verbose:
        print(f"[DEBUG] Found {len(dynamic_urls)} dynamic links via XHR/Fetch")
    return list(dynamic_urls)
    
