# validator.py
"""
Valida endpoints usando asyncio e aiohttp para paralelismo eficiente.
Inclui:
- Timeout
- Delay entre batches
- Filtragem de status válidos
- Verbose mode
"""

import asyncio
import aiohttp
from urllib.parse import urlparse

# Status considerados "válidos" para recon
VALID_STATUS = {200, 201, 204, 301, 302, 401, 403, 405, 500}


async def fetch(session, url, semaphore, delay=0.1, verbose=False):
    """
    Faz requisição GET assíncrona a um endpoint com timeout e delay
    """
    async with semaphore:
        try:
            async with session.get(url, timeout=5, ssl=False) as resp:
                status = resp.status
                if verbose:
                    print(f"[+] Checking {url} -> {status}")
                await asyncio.sleep(delay)  # delay entre requisições
                return url, status
        except asyncio.TimeoutError:
            if verbose:
                print(f"[!] Timeout {url}")
            return url, None
        except aiohttp.ClientError as e:
            if verbose:
                print(f"[!] Error {url}: {e}")
            return url, None


async def validate_all(endpoints, max_concurrent=5, delay=0.1, verbose=False):
    """
    Valida todos os endpoints usando asyncio com limite de concorrência
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    connector = aiohttp.TCPConnector(limit_per_host=max_concurrent)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [
            fetch(session, url, semaphore, delay, verbose)
            for url in endpoints
        ]
        results = await asyncio.gather(*tasks)
        # Filtra apenas status válidos
        return [(url, status) for url, status in results if status in VALID_STATUS]


def validate_endpoints(endpoints, threads=5, delay=0.1, verbose=False):
    """
    Função de entrada que roda a validação assíncrona
    """
    return asyncio.run(validate_all(endpoints, max_concurrent=threads, delay=delay, verbose=verbose))
