"""Constantes de conexión para SUNAT."""

SUNAT_BASE = "https://e-consultaruc.sunat.gob.pe"
SUNAT_SESSION_URL = SUNAT_BASE + "/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp"
SUNAT_URL = SUNAT_BASE + "/cl-ti-itmrconsruc/jcrS00Alias"

DEFAULT_HEADERS = {
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": '"Not-A.Brand";v="24", "Chromium";v="146"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept-Language": "es-ES,es;q=0.9",
    "Origin": "https://e-consultaruc.sunat.gob.pe",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/146.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
        "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    ),
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

DEFAULT_TOKEN = "j9r9v43x4y96c9efegzd5ndrzey2o4ojofrf6kaw5u7jw8cac36u"
