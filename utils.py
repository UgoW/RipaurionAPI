import asyncio
import csv
from urllib.parse import urlparse
import tldextract
from tqdm import tqdm  

from services.network import *
from services.dom import *

SEM = asyncio.Semaphore(100)

def fast_features(url: str) -> dict:
    ext = tldextract.extract(url)
    hostname = urlparse(url).hostname or ""
    return {
        "HttpsInHostname": int("https" in hostname.lower()),
        "UrlLength": len(url),
        "SubdomainLevel": hostname.count(".") - 1 if hostname else 0,
        "IpAddress": int(is_ip_address(url)),
        "Punycode": int("xn--" in hostname.lower()),
        "QueryLength": len(urlparse(url).query),
    }

async def slow_features(url: str) -> dict:
    async with SEM:
        try:
            domain = domaine_extract(url)
            return {
                #1 "DomainAge": domain_age(domain), 
                #2 "CertificateAge": cert_age_days(url),
                #3 "NbExternalLinks": await external_link_ratio(url),
                #4 "form_mismatch": await form_mismatch(url),
                 "TTL": ttl(domain),
                # "Redirects": redirects(url),
            }
        except Exception:
            return {
                "DomainAge": 0,
                "CertificateAge": 0,
                "NbExternalLinks": 0,
                "form_mismatch": 0,
                "TTL": 0,
                "Redirects": 0,
            }

def domaine_extract(url: str) -> str:
    ext = tldextract.extract(url)
    if ext.domain and ext.suffix:
        return f"{ext.domain}.{ext.suffix}"
    return urlparse(url).netloc

async def json_result(url: str) -> dict:
    data = fast_features(url)
    data.update(await slow_features(url))
    return data

async def process_csv_input_to_dataset(inputfile: str, outputfile: str, key: str = "url"):
    with open(inputfile, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        urls = [row[key] for row in reader if key in row]

    results = []
    # tqdm pour afficher une barre de progression
    for url in tqdm(urls, desc="Processing URLs"):
        res = await json_result(url)
        results.append(res)

    fieldnames = results[0].keys() if results else []
    with open(outputfile, "w", newline="", encoding="utf-8") as out_csv:
        writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

if __name__ == "__main__":
    import sys
    inputfile = sys.argv[1] if len(sys.argv) > 1 else "cleaned_urls.csv"
    outputfile = sys.argv[2] if len(sys.argv) > 2 else "output.csv"
    asyncio.run(process_csv_input_to_dataset(inputfile, outputfile))
