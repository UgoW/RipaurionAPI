# services/url/dom.py
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import tldextract

def get_registered_domain(url: str) -> str:
    ext = tldextract.extract(url)
    if ext.domain and ext.suffix:
        return f"{ext.domain}.{ext.suffix}"
    return urlparse(url).netloc

async def fetch_html(url: str, timeout: int = 10) -> str:
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.text

def extract_links(base_url: str, html: str):
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all("a", href=True)
    number_of_links = len(anchors)
    print(f"Extracted {number_of_links} links from {base_url}")
    links = [urljoin(base_url, a["href"]) for a in anchors]
    return links

def external_link_ratio(base_url: str, html: str) -> float:
    links = extract_links(base_url, html)
    if not links:
        return 0.0
    
    base_domain = get_registered_domain(base_url)
    external = 0
    for link in links:
        print(f"Processing link: {link}")
        try:
            if get_registered_domain(link) != base_domain:
                external += 1
        except Exception:
            continue
    return external / len(links) * 100


def form_mismatch(url: str) -> int:
    try:
        html = fetch_html(url)
        soup = BeautifulSoup(html, "html.parser")
        forms = soup.find_all("form", action=True)
        for form in forms:
            action = form["action"]
            action_url = urljoin(url, action)
            if get_registered_domain(action_url) != get_registered_domain(url):
                return 1
        return 0
    except Exception as e:
        print(f"Error fetching or parsing HTML for {url}: {e}")
        return 0