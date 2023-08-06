from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode


def add_params(url_str, params):

    url = urlparse(url_str)
    q = url.query

    qdic = dict(parse_qsl(q))
    qdic.update(params)

    qstr = urlencode(qdic)

    url_parts = list(url)
    url_parts[4] = qstr

    return urlunparse(url_parts)