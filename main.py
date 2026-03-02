# main.py
"""
Endpoint Hunter 1.2
JavaScript Endpoint Extractor e HTML link checker assíncrono.
"""

import argparse
from hunter.crawler import get_html, extract_scripts, fetch_js_files, extract_html_links
from hunter.extractor import extract_endpoints
from hunter.validator import validate_endpoints

def main():
    parser = argparse.ArgumentParser(
        description="Endpoint Hunter - JavaScript & HTML Endpoint Extractor"
    )

    parser.add_argument("-u", "--url", required=True, help="Target URL (ex: https://site.com)")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Max concurrent requests (default: 5)")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between requests in seconds (default: 0.1)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug output")

    args = parser.parse_args()
    target = args.url

    print(f"[+] Target: {target}")

    # 1 - Baixar HTML
    html = get_html(target, verbose=args.verbose)

    # 2 - Extrair links do HTML
    html_links = extract_html_links(html, target, verbose=args.verbose)
    print(f"[+] Found {len(html_links)} HTML links")

    # 3 - Extrair JS
    scripts = extract_scripts(html, target, verbose=args.verbose)
    print(f"[+] Found {len(scripts)} internal JS files")

    # 4 - Baixar JS
    js_contents = fetch_js_files(scripts, verbose=args.verbose)

    # 5 - Extrair endpoints do JS
    js_endpoints = extract_endpoints(js_contents, target, verbose=args.verbose)
    print(f"[+] Raw JS endpoints found: {len(js_endpoints)}")

    # 6 - Combinar HTML links + JS endpoints
    all_endpoints = set(js_endpoints) | set(html_links)
    print(f"[+] Total unique endpoints: {len(all_endpoints)}")

    # 7 - Validar endpoints assíncrono
    print("\n[+] Validating endpoints (excluding 404)...\n")
    results = validate_endpoints(
        all_endpoints,
        threads=args.threads,
        delay=args.delay,
        verbose=args.verbose
    )

    # 8 - Mostrar resultados
    for url, status in results:
        print(f"[{status}] {url}")


if __name__ == "__main__":
    main()
