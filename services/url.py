# services/url/service.py
from urllib.parse import urlparse


# --- Feature functions ---

def url_length(url: str) -> int:
    return len(url)

def path_level(url: str) -> int:
    """Nombre de segments de chemin dans l’URL"""
    parsed = urlparse(url)
    if parsed.path:
        return len([segment for segment in parsed.path.split('/') if segment])
    return 0

def num_dash(url: str) -> int:
    return url.count('-')

def num_dash_in_hostname(url: str) -> int:
    parsed = urlparse(url)
    return parsed.hostname.count('-') if parsed.hostname else 0

def has_tilde_symbol(url: str) -> int:
    return 1 if '~' in url else 0

def num_underscore(url: str) -> int:
    return url.count('_')

def sub_domain_level(url: str) -> int:
    """Compte le nombre de sous-domaines (ex: a.b.c.com → 2)"""
    parsed = urlparse(url)
    if parsed.hostname:
        parts = parsed.hostname.split('.')
        return max(0, len(parts) - 2)
    return 0

def num_percent(url: str) -> int:
    return url.count('%')

def num_query_components(url: str) -> int:
    parsed = urlparse(url)
    if parsed.query:
        return len(parsed.query.split('&'))
    return 0

def num_hash(url: str) -> int:
    return url.count('#')

def num_numeric_chars(url: str) -> int:
    return sum(c.isdigit() for c in url)

def num_dots(url: str) -> int:
    return url.count('.')

def num_ampersand(url: str) -> int:
    return url.count('&')


def uses_https(url: str) -> int:
    """Retourne 1 si HTTPS, sinon 0"""
    return 1 if url.startswith("https://") else 0

def domain_in_subdomain(url: str) -> int:
    """Vrai si le domaine est imbriqué dans un sous-domaine"""
    parsed = urlparse(url)
    if parsed.hostname:
        parts = parsed.hostname.split('.')
        return 1 if len(parts) > 2 else 0
    return 0

def domain_in_path(url: str) -> int:
    """Vrai si le domaine apparaît dans le chemin (souvent phishing)"""
    parsed = urlparse(url)
    if parsed.hostname and parsed.path:
        return 1 if parsed.hostname in parsed.path else 0
    return 0




async def dom_features(url: str) -> dict:
        html = await dom.fetch_html(url)
        external_ratio = dom.external_link_ratio(url, html)
        return round(external_ratio, 2)
    

def at_symbol(url: str) -> int:
    return 1 if '@' in url else 0

def uses_http(url: str) -> int:
    return 1 if url.startswith("http://") else 0

def is_ip_address(url) -> int:
    parsed = urlparse(url)
    if parsed.hostname:
        parts = parsed.hostname.split('.')
        if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
            return 1
    return 0

def hostname_length(url: str) -> int:
    parsed = urlparse(url)
    return len(parsed.hostname) if parsed.hostname else 0

def path_length(url: str) -> int:
    parsed = urlparse(url)
    return len(parsed.path) if parsed.path else 0

def query_length(url: str) -> int:
    parsed = urlparse(url)
    return len(parsed.query) if parsed.query else 0

def double_slash_in_path(url: str) -> int:
    parsed = urlparse(url)
    return 1 if '//' in parsed.path else 0


def is_punycode(url: str) -> int:
    parsed = urlparse(url)
    return 1 if parsed.hostname and parsed.hostname.startswith('xn--') else 0