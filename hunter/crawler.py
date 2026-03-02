# crawler.py
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from hunter.config import DEFAULT_HEADERS, TIMEOUT

# Para JS dinâmico
from playwright.sync_api import sync_playwright

def fetch_html(url, verbose=False):
    """Busca HTML inicial via requests (fallback)"""
    if verbose:
        print(f"[+] Fetching HTML from {url}")
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    return response.text

def extract_html_links(html, base_url, verbose=False):
    """Extrai <a>, <form>, <link> do HTML"""
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for tag in soup.find_all("a", href=True):
        links.add(urljoin(base_url, tag["href"]))
    for tag in soup.find_all("form", action=True):
        links.add(urljoin(base_url, tag["action"]))
    for tag in soup.find_all("link", href=True):
        links.add(urljoin(base_url, tag["href"]))
    if verbose:
        print(f"[DEBUG] Found {len(links)} HTML links")
    return list(links)

def extract_scripts(html, base_url, verbose=False):
    """Extrai scripts internos e externos"""
    soup = BeautifulSoup(html, "html.parser")
    scripts = []
    for script in soup.find_all("script", src=True):
        scripts.append(urljoin(base_url, script["src"]))
    if verbose:
        print(f"[DEBUG] Found {len(scripts)} JS files")
    return list(set(scripts))

def fetch_js_files(script_urls, verbose=False):
    """Baixa JS como texto"""
    js_contents = []
    for url in script_urls:
        try:
            if verbose:
                print(f"[+] Fetching JS: {url}")
            r = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
            if r.status_code == 200:
                js_contents.append(r.text)
        except Exception as e:
            if verbose:
                print(f"[!] Failed {url}: {e}")
    return js_contents

def fetch_dynamic_links(url, verbose=False, wait_time=3000):
    """Executa JS dinâmico usando Playwright e captura links do DOM"""
    links = set()
    if verbose:
        print(f"[+] Launching browser for dynamic JS: {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(wait_time)  # espera JS carregar
        # coleta todos os <a href="">
        for a in page.query_selector_all("a[href]"):
            href = a.get_attribute("href")
            if href:
                links.add(href)
        browser.close()
    if verbose:
        print(f"[DEBUG] Dynamic links found: {len(links)}")
    return [urljoin(url, l) for l in links]
