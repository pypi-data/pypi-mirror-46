def starts_with_http(str):
    return str.startswith('http://')


def starts_with_https(str):
    return str.startswith('https://')


def add_http_if_missing(url):
    if not starts_with_http(url) and not starts_with_https(url):
        url = 'http://' + url
    return url
