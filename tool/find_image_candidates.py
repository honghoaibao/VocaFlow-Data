#!/usr/bin/env python3
"""Find and validate Wikimedia Commons image candidates for VocaFlow.

Human-assisted editorial tool only: it never modifies published content and never
chooses an image automatically. Uses Python standard library; no API key required.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

API_URL = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = (
    "VocaFlowContentEditor/1.0 "
    "(https://github.com/honghoaibao/VocaFlow-Data)"
)
IMAGE_HOSTS = {"upload.wikimedia.org", "thumb.wikimedia.org"}
ALLOWED_DEFAULT = {"cc0", "public domain", "public domain mark"}
EXT_METADATA = "|".join(
    [
        "Artist",
        "Credit",
        "LicenseShortName",
        "LicenseUrl",
        "UsageTerms",
        "Attribution",
        "AttributionRequired",
        "ImageDescription",
    ]
)


def plain_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    value = re.sub(r"<[^>]*>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def metadata_value(metadata: dict[str, Any], key: str) -> str:
    entry = metadata.get(key, {})
    if not isinstance(entry, dict):
        return ""
    return plain_text(entry.get("value", ""))


def normalized_license(value: str) -> str:
    value = plain_text(value).casefold()
    value = value.replace("creative commons zero", "cc0")
    value = value.replace("public domain mark", "public domain")
    return re.sub(r"\s+", " ", value).strip()


def default_license_eligible(value: str) -> bool:
    """Conservative default is CC0/Public Domain only.

    CC BY, BY-SA, NC, ND, GFDL, and missing licenses are not auto-approved.
    This policy avoids assuming the current app has a license-specific credit UI.
    """
    license_name = normalized_license(value)
    return license_name in ALLOWED_DEFAULT or license_name.startswith("cc0 ")


def get_json(url: str, timeout: int = 20) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status} from Wikimedia API")
        content_type = response.headers.get("Content-Type", "")
        if "json" not in content_type.casefold():
            raise RuntimeError(f"Unexpected API Content-Type: {content_type}")
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("Wikimedia API returned an unexpected JSON shape")
    if "error" in payload:
        raise RuntimeError(f"Wikimedia API error: {payload['error']}")
    return payload


def verify_direct_image(url: str, timeout: int = 20) -> dict[str, Any]:
    """Request a small byte range and reject HTML pages masquerading as images."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in IMAGE_HOSTS:
        raise ValueError("Not a trusted HTTPS Wikimedia image URL")

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Range": "bytes=0-1023",
            "Accept": "image/avif,image/webp,image/png,image/jpeg,image/*;q=0.9,*/*;q=0.1",
        },
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        status = response.status
        content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().casefold()
        response.read(1024)
    if status not in (200, 206):
        raise ValueError(f"Direct image returned HTTP {status}")
    if not content_type.startswith("image/"):
        raise ValueError(
            f"Not an image response (Content-Type: {content_type or 'missing'})"
        )
    return {"httpStatus": status, "contentType": content_type}


def search_candidates(
    query: str,
    limit: int = 10,
    width: int = 800,
    include_other_licenses: bool = False,
    verify_urls: bool = True,
) -> list[dict[str, Any]]:
    params = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "generator": "search",
        "gsrnamespace": "6",
        "gsrlimit": str(limit),
        "gsrsearch": f"filetype:bitmap {query}",
        "prop": "imageinfo",
        "iiprop": "url|mime|size|extmetadata",
        "iiurlwidth": str(width),
        "iiextmetadatafilter": EXT_METADATA,
    }
    payload = get_json(API_URL + "?" + urllib.parse.urlencode(params))
    pages = payload.get("query", {}).get("pages", [])
    if not isinstance(pages, list):
        return []

    candidates: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    for page in pages:
        if not isinstance(page, dict):
            continue
        imageinfo_list = page.get("imageinfo", [])
        if not isinstance(imageinfo_list, list) or not imageinfo_list:
            continue

        info = imageinfo_list[0]
        metadata = info.get("extmetadata", {})
        if not isinstance(metadata, dict):
            metadata = {}
        license_name = metadata_value(metadata, "LicenseShortName")
        eligible = default_license_eligible(license_name)
        if not eligible and not include_other_licenses:
            continue

        direct_url = info.get("thumburl") or info.get("url")
        if not isinstance(direct_url, str) or direct_url in seen_urls:
            continue
        seen_urls.add(direct_url)

        expected_mime = info.get("thumbmime") or info.get("mime") or ""
        if not isinstance(expected_mime, str) or not expected_mime.startswith("image/"):
            continue
        if verify_urls:
            try:
                url_check = verify_direct_image(direct_url)
            except (OSError, urllib.error.URLError, ValueError, RuntimeError) as exc:
                print(
                    f"Skipping unverified URL for {page.get('title', 'unknown file')}: {exc}",
                    file=sys.stderr,
                )
                continue
        else:
            url_check = {"httpStatus": None, "contentType": expected_mime}

        author = metadata_value(metadata, "Artist")
        attribution = metadata_value(metadata, "Attribution")
        credit = attribution or author or metadata_value(metadata, "Credit")
        title = plain_text(page.get("title", "")).removeprefix("File:").strip()
        candidates.append(
            {
                "title": title,
                "imageUrl": direct_url,
                "imageSourceUrl": info.get("descriptionurl", ""),
                "imageAuthor": author,
                "imageCredit": credit or "Author/credit not present in API metadata",
                "imageLicense": license_name,
                "imageLicenseUrl": metadata_value(metadata, "LicenseUrl"),
                "imageRightsNote": (
                    "Candidate only. Open the file page and manually confirm the license, "
                    "restrictions, and attribution before publishing."
                ),
                "description": metadata_value(metadata, "ImageDescription"),
                "mime": expected_mime,
                "width": info.get("thumbwidth") or info.get("width"),
                "height": info.get("thumbheight") or info.get("height"),
                "policyEligibleByDefault": eligible,
                "directUrlCheck": url_check,
            }
        )
    return candidates


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Search Wikimedia Commons and return direct, verified image URLs with license metadata. "
            "Published packs are never modified automatically."
        )
    )
    parser.add_argument("query", help="Specific English phrase describing the target visual")
    parser.add_argument("--limit", type=int, default=10, help="API candidates requested (1–25)")
    parser.add_argument("--width", type=int, default=800, help="Thumbnail width (300–1600)")
    parser.add_argument(
        "--include-other-licenses",
        action="store_true",
        help="Include candidates NOT approved by the conservative default license policy",
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip the direct URL HTTP/MIME check (not recommended before publication)",
    )
    parser.add_argument(
        "--output",
        help="Optional JSON output path; otherwise write JSON to stdout",
    )
    args = parser.parse_args()

    if not args.query.strip():
        parser.error("query cannot be blank")
    if not 1 <= args.limit <= 25:
        parser.error("--limit must be between 1 and 25")
    if not 300 <= args.width <= 1600:
        parser.error("--width must be between 300 and 1600")

    try:
        candidates = search_candidates(
            query=args.query.strip(),
            limit=args.limit,
            width=args.width,
            include_other_licenses=args.include_other_licenses,
            verify_urls=not args.no_verify,
        )
    except (OSError, urllib.error.URLError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    output = {
        "query": args.query.strip(),
        "source": "Wikimedia Commons API",
        "requestedLimit": args.limit,
        "results": candidates,
        "editorialReminder": (
            "Search relevance is not proof of meaning, rights, or long-term availability. "
            "Open the file page, inspect the actual image, verify its license/restrictions, "
            "then manually approve one candidate. Do not publish this candidate output directly."
        ),
    }
    text = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(text)
    else:
        sys.stdout.write(text)
    print(f"Found {len(candidates)} candidates. Human review is still required.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
