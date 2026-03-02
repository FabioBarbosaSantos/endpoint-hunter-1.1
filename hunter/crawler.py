import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_HEADERS = {"User-Agent": "EndpointHunter/1.1"}
TIMEOUT = 10

def normalize_target(url):
    parsed = urlparse(url)
    if not parsed.scheme:
        https_url = "https://" + url
        try:
            requests.get(https_url, timeout=5, headers=DEFAULT_HEADERS, verify=False)
            url = https_url
        except:
            url = "http://" + url
    parsed = urlparse(url)
    cleaned = parsed._replace(fragment="")
    return urlunparse(cleaned)

def fetch_html(url, verbose=False):
    try:
        if verbose: print(f"[+] Requesting HTML: {url}")
        r = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT, verify=False)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        print(f"[!] Error fetching HTML: {e}")
        return ""

def extract_html_links(html, base_url, verbose=False):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    # <a href="">
    for tag in soup.find_all("a", href=True):
        full_url = urljoin(base_url, tag["href"])
        links.add(full_url)

    # <form action="">
    for tag in soup.find_all("form", action=True):
        full_url = urljoin(base_url, tag["action"])
        links.add(full_url)

    # <link href="">
    for tag in soup.find_all("link", href=True):
        full_url = urljoin(base_url, tag["href"])
        links.add(full_url)

    if verbose:
        print(f"Found {len(links)} HTML links")
    return list(links)

def extract_scripts(html, base_url, verbose=False):
    soup = BeautifulSoup(html, "html.parser")
    scripts = []
    for script in soup.find_all("script", src=True):
        full_url = urljoin(base_url, script["src"])
        scripts.append(full_url)
        if verbose: print(f"Found JS file: {full_url}")
    return list(set(scripts))

def fetch_js_files(script_urls, verbose=False):
    js_contents = []
    for url in script_urls:
        try:
            if verbose: print(f"[+] Fetching JS: {url}")
            r = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT, verify=False)
            if r.status_code == 200:
                js_contents.append(r.text)
        except requests.RequestException as e:
            if verbose: print(f"[!] Failed to fetch {url}: {e}")
    return js_contents
