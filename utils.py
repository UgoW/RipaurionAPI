
from services.network import *
from services.url import *  
from services.dom import *

async def json_result(url: str) -> dict:
    features = {
        "HttpsInHostname": uses_https(url),
        "UrlLength": url_length(url),
        "SubdomainLevel": sub_domain_level(url),
        "DomainAge": domain_age(domaine_extract(url)),
        "IpAddress": is_ip_address(url),
        "Punycode": is_punycode(url),
        "form_mismatch": form_mismatch(url),
        "CertificateAge": cert_age_days(url),
        "NbExternalLinks": external_link_ratio(url),
        "QueryLength": query_length(url),
        "TTL": ttl(domaine_extract(url)), 
        "Redirects": redirects(url),
    }
    return features


def domaine_extract(url: str) -> str:
    ext = tldextract.extract(url)
    if ext.domain and ext.suffix:
        return f"{ext.domain}.{ext.suffix}"
    return urlparse(url).netloc