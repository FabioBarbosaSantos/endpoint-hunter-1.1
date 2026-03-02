import re
from urllib.parse import urljoin, urlparse

ENDPOINT_REGEX = re.compile(r"""
["']                        # abre aspas
(
(?:\/|\.\.?\/)?             # / ou ./ ou ../
[a-zA-Z0-9_\-\/\.]+         # path
)
["']
""", re.VERBOSE)

def extract_endpoints(js_contents, base_url, verbose=False):
    endpoints = set()
    for content in js_contents:
        for match in ENDPOINT_REGEX.findall(content):
            full_url = urljoin(base_url, match)
            endpoints.add(full_url)
            if verbose: print(f"[DEBUG] Extracted endpoint: {full_url}")
    return list(endpoints)
