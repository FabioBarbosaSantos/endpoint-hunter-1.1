import argparse
from urllib.parse import urlparse

from hunter.crawler import fetch_html, extract_internal_js
from hunter.extractor import fetch_js, extract_endpoints, normalize_endpoints
from hunter.validator import filter_internal, validate_endpoints


def normalize_target(url):
    if not url.startswith("http"):
        url = "http://" + url
    return url


def main():
    parser = argparse.ArgumentParser(description="Endpoint Hunter")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads")

    args = parser.parse_args()

    target = normalize_target(args.url)
    print(f"[+] Target: {target}")

    # HTML
    html = fetch_html(target)

    # JS internos
    js_files = extract_internal_js(html, target)
    print(f"[+] Found {len(js_files)} internal JS files")

    all_endpoints = set()

    # Extrai endpoints
    for js in js_files:
        print(f"[+] Fetching JS: {js}")
        js_content = fetch_js(js)
        endpoints = extract_endpoints(js_content)
        normalized = normalize_endpoints(endpoints, target)
        all_endpoints.update(normalized)

    print(f"[+] Raw endpoints found: {len(all_endpoints)}")

    # Remove externos
    internal_only = filter_internal(all_endpoints, target)
    print(f"[+] Internal endpoints: {len(internal_only)}")

    # Multithread validation
    print("\n[+] Valid endpoints (excluding 404):\n")
    valid = validate_endpoints(internal_only, threads=args.threads)

    for url, status in sorted(valid):
        print(f"[{status}] {url}")


if __name__ == "__main__":
    main()
