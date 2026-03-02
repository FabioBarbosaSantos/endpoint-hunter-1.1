import argparse
from hunter.crawler import (
    fetch_html,
    extract_scripts,
    fetch_js_files,
    extract_html_links,
    fetch_dynamic_links
)
from hunter.extractor import extract_endpoints
from hunter.validator import validate_endpoints

def main():
    parser = argparse.ArgumentParser(
        description="Endpoint Hunter 1.1 - JS dynamic + HTML endpoints"
    )
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Concurrent requests")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between requests")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    target = args.url
    print(f"[+] Target: {target}")

    # 1 - HTML estático
    html = fetch_html(target, verbose=args.verbose)
    html_links = extract_html_links(html, target, verbose=args.verbose)

    # 2 - HTML dinâmico
    dynamic_links = fetch_dynamic_links(target, verbose=args.verbose)
    all_html_links = list(set(html_links) | set(dynamic_links))
    print(f"[+] Found {len(all_html_links)} HTML links (static + dynamic)")

    # 3 - Scripts JS
    scripts = extract_scripts(html, target, verbose=args.verbose)
    js_contents = fetch_js_files(scripts, verbose=args.verbose)
    print(f"[+] Found {len(js_contents)} JS files")

    # 4 - Endpoints do JS
    js_endpoints = extract_endpoints(js_contents, target, verbose=args.verbose)
    print(f"[+] Raw JS endpoints found: {len(js_endpoints)}")

    # 5 - Unir todos endpoints
    all_endpoints = list(set(all_html_links) | set(js_endpoints))
    print(f"[+] Total unique endpoints: {len(all_endpoints)}")

    # 6 - Validar endpoints
    print("\n[+] Validating endpoints (excluding 404)...\n")
    results = validate_endpoints(all_endpoints, target, threads=args.threads, delay=args.delay, verbose=args.verbose)

    for url, status in results:
        print(f"[{status}] {url}")

if __name__ == "__main__":
    main()
