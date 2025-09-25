import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import tldextract

def get_registered_domain(url: str) -> str:
    ext = tldextract.extract(url)
    if ext.domain and ext.suffix:
        return f"{ext.domain}.{ext.suffix}"
    return urlparse(url).netloc

async def fetch_html(url: str, timeout: int = 5) -> str:
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.text
    except Exception:
        return ""

def extract_links(base_url: str, html: str):
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all("a", href=True)
    return [urljoin(base_url, a["href"]) for a in anchors]

async def external_link_ratio(base_url: str) -> float:
    try:
        html = await fetch_html(base_url)
        links = extract_links(base_url, html)
        if not links:
            return 0.0
        base_domain = get_registered_domain(base_url)
        external = sum(1 for link in links if get_registered_domain(link) != base_domain)
        return external / len(links) * 100
    except Exception:
        return 0.0

async def form_mismatch(url: str) -> int:
    try:
        html = await fetch_html(url)
        if not html:
            return 0
        soup = BeautifulSoup(html, "html.parser")
        forms = soup.find_all("form", action=True)
        base_domain = get_registered_domain(url)
        for form in forms:
            action_url = urljoin(url, form["action"])
            if get_registered_domain(action_url) != base_domain:
                return 1
        return 0
    except Exception:
        return 0
