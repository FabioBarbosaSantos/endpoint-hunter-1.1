import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from hunter.config import DEFAULT_HEADERS, TIMEOUT

def validate_endpoints(endpoints, threads=5, delay=0.1, verbose=False):
    results = []

    def check(url):
        try:
            r = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT, verify=False)
            return (url, r.status_code)
        except requests.RequestException:
            return (url, "ERR")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_url = {executor.submit(check, ep): ep for ep in endpoints}
        for future in as_completed(future_to_url):
            url, status = future.result()
            results.append((url, status))
            if verbose:
                print(f"[+] Checking {url} -> {status}")
            time.sleep(delay)
    return results
