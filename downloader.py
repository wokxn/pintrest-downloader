import re
import time
import requests
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

download_folder = Path("downloads")
download_folder.mkdir(exist_ok=True)

with open("urls.txt") as f:
    urls = [line.strip() for line in f if line.strip()]

print(f"Loaded {len(urls)} URLs")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

session = requests.Session()
session.headers.update(HEADERS)

OG_IMAGE_RE = re.compile(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](https://[^"\']+)["\']', re.IGNORECASE)

OG_IMAGE_RE2 = re.compile(r'<meta[^>]+content=["\'](https://[^"\']+)["\'][^>]+property=["\']og:image["\']', re.IGNORECASE)

def get_og_image(url):
    r = session.get(url, timeout=15)
    r.raise_for_status()
    html = r.text
    m = OG_IMAGE_RE.search(html) or OG_IMAGE_RE2.search(html)
    return m.group(1) if m else None

def process_url(index, url):
    try:
        img_url = get_og_image(url)
        if not img_url:
            return f"[{index}] FAILED – no og:image found"

        img_url = re.sub(r'/\d+x/', '/originals/', img_url)

        img_data = session.get(img_url, timeout=15).content
        if len(img_data) < 1000:
            return f"[{index}] FAILED – image too small (likely blocked)"

        ext = "jpg" if "jpg" in img_url.lower() else "png" if "png" in img_url.lower() else "jpg"
        filename = f"img_{index:04d}.{ext}"
        (download_folder / filename).write_bytes(img_data)
        return f"[{index}] Saved → {filename}"

    except Exception as e:
        return f"[{index}] Error: {e}"

MAX_THREADS = 5

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = [executor.submit(process_url, i, url) for i, url in enumerate(urls, 1)]
    for f in as_completed(futures):
        print(f.result())
