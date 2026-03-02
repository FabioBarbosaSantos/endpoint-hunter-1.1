import re
from urllib.parse import urljoin

def extract_endpoints(js_contents, base_url, verbose=False):
    endpoints = set()
    url_regex = r"""(?:"|')(\/[^\s"'<>]+)(?:"|')"""
    
    for content in js_contents:
        matches = re.findall(url_regex, content)
        for m in matches:
            full_url = urljoin(base_url, m)
            endpoints.add(full_url)
    if verbose:
        print(f"[DEBUG] Extracted {len(endpoints)} JS endpoints")
    return list(endpoints)
