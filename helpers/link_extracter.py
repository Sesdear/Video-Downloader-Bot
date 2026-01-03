from urllib.parse import urlparse

async def split_link(link: str) -> str:
    parsed = urlparse(link)
    return parsed.netloc
