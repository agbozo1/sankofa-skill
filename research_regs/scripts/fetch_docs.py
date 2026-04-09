#!/usr/bin/env python3
"""
Sankofa — fetch_docs.py
Download regulatory PDFs from a list of URLs into a local directory.

Called by the SKILL.md auto-fetch step after Claude discovers document URLs
via WebSearch / the registry.
"""

import argparse
import hashlib
import re
import sys
import time
from pathlib import Path
from urllib.parse import unquote, urlparse

try:
    import requests
except ImportError:
    print("Error: requests not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/pdf,application/octet-stream,*/*",
}
TIMEOUT = 30
MAX_RETRIES = 2


def safe_filename(url: str, content_disposition: str = "") -> str:
    """Derive a safe local filename from URL or Content-Disposition header."""
    # Try Content-Disposition first
    if content_disposition:
        m = re.search(r'filename\*?=["\']?(?:UTF-8\'\')?([^"\';\r\n]+)', content_disposition, re.I)
        if m:
            name = unquote(m.group(1).strip().strip('"\''))
            if name.lower().endswith(".pdf"):
                return re.sub(r'[^\w\-. ]', '_', name)

    # Fall back to URL path
    path = unquote(urlparse(url).path)
    name = Path(path).name
    if name and name.lower().endswith(".pdf"):
        return re.sub(r'[^\w\-. ]', '_', name)

    # Last resort: hash of URL
    return hashlib.md5(url.encode()).hexdigest()[:12] + ".pdf"


def download_pdf(url: str, output_dir: Path, session: requests.Session) -> tuple[bool, str]:
    """
    Download a single PDF. Returns (success, local_path_or_error_message).
    Retries up to MAX_RETRIES on transient failures.
    Skips SSL verification on government sites that commonly have cert issues.
    """
    for attempt in range(1, MAX_RETRIES + 2):
        try:
            resp = session.get(
                url,
                headers=HEADERS,
                timeout=TIMEOUT,
                verify=False,       # many African govt sites have cert issues
                allow_redirects=True,
                stream=True,
            )

            if resp.status_code == 404:
                return False, f"404 Not Found"
            if resp.status_code == 403:
                return False, f"403 Forbidden — site blocks direct download"
            resp.raise_for_status()

            content_type = resp.headers.get("Content-Type", "")
            if "html" in content_type.lower() and "pdf" not in content_type.lower():
                # Got an HTML page (login wall, JS redirect, etc.)
                return False, "Got HTML instead of PDF — site may require authentication"

            filename = safe_filename(url, resp.headers.get("Content-Disposition", ""))
            dest = output_dir / filename

            # Avoid overwriting if already downloaded
            if dest.exists():
                return True, str(dest)

            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)

            size_kb = dest.stat().st_size / 1024
            if size_kb < 5:
                dest.unlink()
                return False, f"File too small ({size_kb:.1f} KB) — likely an error page"

            return True, str(dest)

        except requests.exceptions.SSLError:
            # Already using verify=False, so this is a deeper network issue
            return False, "SSL error — network may be blocking the request"
        except requests.exceptions.ConnectionError:
            if attempt <= MAX_RETRIES:
                time.sleep(2 * attempt)
                continue
            return False, "Connection error after retries"
        except requests.exceptions.Timeout:
            if attempt <= MAX_RETRIES:
                time.sleep(2)
                continue
            return False, "Timeout"
        except Exception as e:
            return False, str(e)

    return False, "Failed after retries"


def main():
    ap = argparse.ArgumentParser(description="Sankofa PDF Fetcher")
    ap.add_argument("--urls", nargs="+", required=True, help="PDF URLs to download")
    ap.add_argument("--output", required=True, help="Directory to save PDFs into")
    args = ap.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Suppress InsecureRequestWarning (expected for govt sites)
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    session = requests.Session()
    session.headers.update(HEADERS)

    results = {"success": [], "failed": []}

    for url in args.urls:
        url = url.strip()
        if not url:
            continue
        print(f"  Fetching: {url}", file=sys.stderr, end=" ... ", flush=True)
        ok, msg = download_pdf(url, output_dir, session)
        if ok:
            print(f"saved → {Path(msg).name}", file=sys.stderr)
            results["success"].append({"url": url, "path": msg})
        else:
            print(f"FAILED ({msg})", file=sys.stderr)
            results["failed"].append({"url": url, "reason": msg})

    print(f"\nDownloaded: {len(results['success'])} | Failed: {len(results['failed'])}", file=sys.stderr)

    if results["failed"]:
        print("\nFailed URLs:", file=sys.stderr)
        for f in results["failed"]:
            print(f"  {f['url']} — {f['reason']}", file=sys.stderr)

    # Print downloaded paths to stdout for the skill to read
    for s in results["success"]:
        print(s["path"])

    if not results["success"]:
        print("Error: No documents downloaded successfully.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
