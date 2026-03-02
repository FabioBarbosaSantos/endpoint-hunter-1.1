import re
from urllib.parse import urljoin

def fetch_js(url):
    import requests
    try:
        r = requests.get(url, timeout=10)
        return r.text
    except:
        return ""

def extract_endpoints(js_content):
    # regex simples para endpoints
    pattern = r'["\']((?:\/|\.\.\/|\.\.|\w)[^"\']+)["\']'
    matches = re.findall(pattern, js_content)
    return set(matches)

def normalize_endpoints(endpoints, base_url):
    normalized = set()
    for ep in endpoints:
        full = urljoin(base_url, ep)
        normalized.add(full)
    return normalized
