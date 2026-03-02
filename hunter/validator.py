import requests
from urllib.parse import urlparse
import time

VALID_STATUS = {200, 201, 204, 301, 302, 401, 403, 405, 500}

def is_internal(url, base_domain):
    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        return False
    return hostname == base_domain or hostname.endswith("." + base_domain)

def validate_endpoints(endpoints, base_url, threads=5, delay=0.1, verbose=False):
    base_domain = urlparse(base_url).hostname
    results = []

    for url in endpoints:
        parsed = urlparse(url)
        if not is_internal(url, base_domain):
            continue
        try:
            if verbose: print(f"[+] Checking {url}")
            r = requests.get(url, timeout=5, verify=False)
            if r.status_code in VALID_STATUS:
                results.append((url, r.status_code))
            time.sleep(delay)
        except requests.RequestException:
            continue
    return results
