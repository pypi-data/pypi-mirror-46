PROVIDERS = {
    "japscan": {
        "BASE_URL": "https://www.japscan.to/lecture-en-ligne/",
        "URL_MIDDLE": "",
        "URL_SUFFIX": ".html",
        "PAGE_PARAMETER_TYPE": "file",
        "IMG_REGEX": '<img\s+[^>]*src="([^"]*[0-9]+\.(?:jpg|png|jpeg))"[^>]*>',
        "CORRECT_EXT": ["png", "jpg", "jpeg"]
    },
    "scantrad": {
        "BASE_URL": "https://scantrad.fr/mangas/",
        "URL_MIDDLE": "",
        "PAGE_PARAMETER_TYPE": "option",
        "URL_SUFFIX": ".html",
        "IMG_REGEX": '<img\s+[^>]*src="([^"]*[0-9]+\.(?:jpg|png|jpeg))"[^>]*>',
        "CORRECT_EXT": ["png", "jpg", "jpeg"]
    },
    "jaiminibox": {
        "BASE_URL": "https://www.japscan.cc/lecture-en-ligne/",
        "URL_MIDDLE": "",
        "URL_SUFFIX": ".html",
        "IMG_REGEX": '<img\s+[^>]*src="([^"]*[0-9]+\.(?:jpg|png|jpeg))"[^>]*>',
        "CORRECT_EXT": ["png", "jpg", "jpeg"]
    }
}


def get_provider(key):
    return PROVIDERS.get(key, PROVIDERS.get("scantrad"))
