import datetime
import ipaddress

def is_ip_address(url: str) -> bool:
    from urllib.parse import urlparse
    try:
        host = urlparse(url).hostname
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False

def domain_age(domain: str) -> int:
    try:
        import whois
        if not domain or is_ip_address(domain):
            return 0
        w = whois.whois(domain)
        creation_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
        if not creation_date:
            return 0
        return (datetime.datetime.now() - creation_date).days // 365
    except Exception:
        return 0

def cert_age_days(url: str) -> int:
    import ssl
    import socket
    from urllib.parse import urlparse

    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return 0
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                not_before = datetime.datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                return (datetime.datetime.now() - not_before).days
    except Exception:
        return 0

def ttl(domain: str) -> int:
    import dns.resolver
    try:
        import ipaddress
        if is_ip_address(domain) or ipaddress.ip_address(domain):
            return 0
        answers = dns.resolver.resolve(domain, 'A')
        return answers.rrset.ttl if answers.rrset else 0
    except Exception:
        return 0

def redirects(url: str) -> int:
    import httpx
    try:
        with httpx.Client(follow_redirects=True, timeout=5) as client:
            r = client.get(url)
            return len(r.history)
    except Exception:
        return 0
