import argparse
from hunter.crawler import fetch_html, extract_scripts, fetch_js_files, extract_html_links, normalize_target
from hunter.extractor import extract_endpoints
from hunter.validator import validate_endpoints

def main():
    parser = argparse.ArgumentParser(
        description="Endpoint Hunter 1.1"
    )
    parser.add_argument("-u", "--url", required=True, help="Target URL (ex: https://site.com)")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of threads for validation")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between requests (s)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug output")
    
    args = parser.parse_args()
    
    target = normalize_target(args.url)
    print(f"[+] Target: {target}")

    # 1 - Baixar HTML
    html = fetch_html(target, verbose=args.verbose)
    if not html:
        print("[!] Could not fetch HTML. Exiting.")
        return

    # 2 - Extrair links internos do HTML
    html_links = extract_html_links(html, target, verbose=args.verbose)

    # 3 - Extrair scripts JS
    scripts = extract_scripts(html, target, verbose=args.verbose)
    print(f"[+] Found {len(scripts)} internal JS files")

    # 4 - Baixar JS
    js_contents = fetch_js_files(scripts, verbose=args.verbose)

    # 5 - Extrair endpoints do JS
    endpoints = extract_endpoints(js_contents, target, verbose=args.verbose)
    print(f"[+] Raw endpoints found: {len(endpoints)}")

    # 6 - Combinar endpoints HTML e JS
    all_endpoints = set(endpoints) | set(html_links)
    print(f"[+] Total unique endpoints: {len(all_endpoints)}\n")

    # 7 - Validar endpoints
    results = validate_endpoints(all_endpoints, target, threads=args.threads, delay=args.delay, verbose=args.verbose)

    print("[+] Valid endpoints (excluding 404):\n")
    for url, status in results:
        print(f"[{status}] {url}")


if __name__ == "__main__":
    main()
