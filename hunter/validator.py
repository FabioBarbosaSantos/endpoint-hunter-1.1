import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

def filter_internal(endpoints, base_url):
    base_domain = urlparse(base_url).netloc
    filtered = set()

    for url in endpoints:
        parsed = urlparse(url)
        if parsed.netloc == base_domain:
            filtered.add(url)

    return filtered

def check_endpoint(url):
    try:
        r = requests.get(url, timeout=5)
        return url, r.status_code
    except:
        return url, None

def validate_endpoints(endpoints, threads=20):
    results = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(check_endpoint, url) for url in endpoints]

        for future in as_completed(futures):
            url, status = future.result()
            if status and status != 404:
                results.append((url, status))

    return results
