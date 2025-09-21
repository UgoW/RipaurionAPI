
from services.url import *  

async def json_result(url: str) -> dict:
    features = {
        "NumDots": num_dots(url),
        "SubdomainLevel": sub_domain_level(url),
        "PathLevel": path_level(url),
        "UrlLength": url_length(url),
        "NumDash": num_dash(url),
        "NumDashInHostname": num_dash_in_hostname(url),
        "AtSymbol": at_symbol(url),
        "TildeSymbol": has_tilde_symbol(url),
        "NumUnderscore": num_underscore(url),
        "NumPercent": num_percent(url),
        "NumQueryComponents": num_query_components(url),
        "NumAmpersand": num_ampersand(url),
        "NumHash": num_hash(url),
        "NumNumericChars": num_numeric_chars(url),
        "NoHttps": uses_http(url),
        "IpAddress": is_ip_address(url),
        "HttpsInHostname": uses_https(url),
        "HostnameLength": hostname_length(url),
        "PathLength": path_length(url),
        "QueryLength": query_length(url),
        "DoubleSlashInPath": double_slash_in_path(url),
    }
    return features