import datetime

def domain_age(domaine:str) -> int:
    # Extract the domain from the URL
    if not domaine:
        return 0

    # Get the creation date of the domain
    creation_date = get_domain_creation_date(domaine)
    if not creation_date:
        return 0

    # Calculate the age of the domain in years
    age = (datetime.now() - creation_date).days // 365
    return age



def get_domain_creation_date(domain: str) -> datetime:
    try:
        import whois
        w = whois.whois(domain)
        if isinstance(w.creation_date, list):
            return w.creation_date[0]
        return w.creation_date
    except Exception as e:
        print(f"Error fetching WHOIS data for {domain}: {e}")
        return None
    

def cert_age_days(url: str) -> int:
    import ssl
    import socket
    from urllib.parse import urlparse

    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        if not hostname:
            return 0

        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                age_days = (datetime.now() - not_before).days
                return age_days
    except Exception as e:
        print(f"Error fetching SSL certificate for {url}: {e}")
        return 0
    

def ttl(domain: str) -> int:
    import dns.resolver
    try:
        answers = dns.resolver.resolve(domain, 'A')
        if answers.rrset is not None:
            return answers.rrset.ttl
        return 0
    except Exception as e:
        print(f"Error fetching TTL for {domain}: {e}")
        return 0
    

def redirects(url: str) -> int:
    import httpx
    try:
        with httpx.Client(follow_redirects=True, timeout=10) as client:
            response = client.get(url)
            return len(response.history)
    except Exception as e:
        print(f"Error fetching redirects for {url}: {e}")
        return 0