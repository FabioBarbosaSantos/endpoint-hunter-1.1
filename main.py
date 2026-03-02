import argparse
from hunter.crawler import (
    fetch_html,
    extract_html_links,
    extract_scripts,
    fetch_js_files,
    fetch_dynamic_links
)
from hunter.extractor import extract_endpoints
from hunter.validator import validate_endpoints

def main():
    parser = argparse.ArgumentParser(description="Endpoint Hunter 1.2 - Static + Dynamic JS")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Threads for validation")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between requests")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    target = args.url
    print(f"[+] Target: {target}")

    # HTML + links
    html = fetch_html(target, verbose=args.verbose)
    html_links = extract_html_links(html, target, verbose=args.verbose)

    # JS estático
    scripts = extract_scripts(html, target, verbose=args.verbose)
    js_contents = fetch_js_files(scripts, verbose=args.verbose)
    js_endpoints = extract_endpoints(js_contents, target, verbose=args.verbose)

    # JS dinâmico (XHR / Fetch)
    dynamic_links = fetch_dynamic_links(target, verbose=args.verbose)

    # Unir tudo
    all_endpoints = set(html_links) | set(js_endpoints) | set(dynamic_links)
    print(f"[+] Total unique endpoints: {len(all_endpoints)}")

    # Validar
    print("\n[+] Validating endpoints (excluding 404)...\n")
    results = validate_endpoints(all_endpoints, threads=args.threads, delay=args.delay, verbose=args.verbose)
    for url, status in results:
        if status != 404:
            print(f"[{status}] {url}")

if __name__ == "__main__":
    main()
