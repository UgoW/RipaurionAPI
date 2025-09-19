from urllib.parse import urlparse

def url_lenf(url: str) -> int:
    return len(url)

def path_depth(url: str) -> int:
    return url.count('/') - 2

def num_dash(url: str) -> int:
    return url.count('-')

def num_dash_hostName(url: str) -> int:
    parsed_url = urlparse(url)
    return parsed_url.hostname.count('-') if parsed_url.hostname else 0

def has_tild_symbol(url: str) -> int:
    return 1 if '~' in url else 0

def num_underscore(url: str) -> int:
    return url.count('_')

def sub_domain_level(url: str) -> int:
    parsed_url = urlparse(url)
    if parsed_url.hostname:
        return parsed_url.hostname.count('.') - 1
    return 0

def num_percent(url: str) -> int:
    return url.count('%')

def num_query_components(url: str) -> int:
    parsed_url = urlparse(url)
    if parsed_url.query:
        return len(parsed_url.query.split('&'))
    return 0

def num_hash(url: str) -> int:
    return url.count('#')

def num_numeric_chars(url: str) -> int:
    return sum(c.isdigit() for c in url)

def no_https(url: str) -> int:
    return 1 if url.startswith('https://') else 0