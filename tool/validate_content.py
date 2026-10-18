#!/usr/bin/env python3
"""Validate the public VocaFlow JSON content repository using Python stdlib only."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PACK_PATH = re.compile(
    r"^assets/vocabulary/packs/[a-z0-9]+(?:_[a-z0-9]+)*_(\d{4}-\d{2}-\d{2})\.json$"
)
ARTICLE_PATH = re.compile(
    r"^assets/editorial/articles/[a-z0-9]+(?:_[a-z0-9]+)*_(\d{4}-\d{2}-\d{2})\.json$"
)
CATALOG_PATH = re.compile(
    r"^assets/discovery/catalog/approved/links-approved-(\d{4}-\d{2}-\d{2})\.json$"
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_json(relative_path: str) -> dict:
    path = Path(relative_path)
    if path.is_absolute() or ".." in path.parts or not relative_path.startswith("assets/"):
        fail(f"Unsafe content path: {relative_path!r}")
    file_path = ROOT / path
    if not file_path.is_file():
        fail(f"Manifest target does not exist: {relative_path}")
    try:
        value = json.loads(file_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"Invalid JSON in {relative_path}: {exc}")
    if not isinstance(value, dict):
        fail(f"Expected a JSON object in {relative_path}")
    return value


def valid_date(value: object) -> bool:
    if not isinstance(value, str) or not DATE.fullmatch(value):
        return False
    from datetime import date
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def validate_vocabulary_and_articles() -> None:
    manifest_path = "assets/content/index.json"
    manifest = read_json(manifest_path)
    if manifest.get("schemaVersion") != 1:
        fail(f"{manifest_path}: schemaVersion must be 1")

    seen_word_ids: set[str] = set()
    for entry in manifest.get("vocabularyPacks", []):
        if not isinstance(entry, dict):
            fail("Each vocabularyPacks entry must be an object")
        path, publish_date = entry.get("path"), entry.get("publishDate")
        match = PACK_PATH.fullmatch(path or "") if isinstance(path, str) else None
        if not match or match.group(1) != publish_date or not valid_date(publish_date):
            fail(f"Invalid vocabulary path/date entry: {entry!r}")
        pack = read_json(path)
        if pack.get("schemaVersion") != 1 or pack.get("status") != "published":
            fail(f"{path}: only schemaVersion 1 and published packs are allowed")
        if pack.get("publishDate") != publish_date or not pack.get("topic") or not pack.get("level"):
            fail(f"{path}: publishDate, topic, and level must be valid")
        words = pack.get("words")
        if not isinstance(words, list) or not words:
            fail(f"{path}: words must be a non-empty list")
        for word in words:
            if not isinstance(word, dict):
                fail(f"{path}: every word must be an object")
            word_id = word.get("id")
            if not isinstance(word_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", word_id):
                fail(f"{path}: invalid word id {word_id!r}")
            if word_id in seen_word_ids:
                fail(f"Duplicate word id across packs: {word_id}")
            seen_word_ids.add(word_id)
            if not isinstance(word.get("word"), str) or not word["word"].strip():
                fail(f"{path}: word {word_id} is missing its word")
            if not isinstance(word.get("meaning"), str) or not word["meaning"].strip():
                fail(f"{path}: word {word_id} is missing its meaning")

    seen_article_ids: set[str] = set()
    for entry in manifest.get("editorialArticles", []):
        if not isinstance(entry, dict):
            fail("Each editorialArticles entry must be an object")
        path, publish_date = entry.get("path"), entry.get("publishDate")
        match = ARTICLE_PATH.fullmatch(path or "") if isinstance(path, str) else None
        if not match or match.group(1) != publish_date or not valid_date(publish_date):
            fail(f"Invalid article path/date entry: {entry!r}")
        article = read_json(path)
        if article.get("schemaVersion") != 1 or article.get("status") != "published":
            fail(f"{path}: only schemaVersion 1 and published articles are allowed")
        if article.get("publishDate") != publish_date or not article.get("title"):
            fail(f"{path}: publishDate and title must be valid")
        article_id = article.get("id")
        if not isinstance(article_id, str) or not re.fullmatch(r"[a-z0-9-]+", article_id):
            fail(f"{path}: invalid article id {article_id!r}")
        if article_id in seen_article_ids:
            fail(f"Duplicate article id: {article_id}")
        seen_article_ids.add(article_id)


def validate_discovery_catalogs() -> None:
    index_path = "assets/discovery/catalog/index.json"
    index = read_json(index_path)
    if index.get("schemaVersion") != 1 or not isinstance(index.get("catalogs"), list):
        fail(f"{index_path}: expected schemaVersion 1 and catalogs list")

    seen_ids: set[str] = set()
    for entry in index["catalogs"]:
        if not isinstance(entry, dict):
            fail("Each catalog entry must be an object")
        path, approval_date = entry.get("path"), entry.get("approvedDate")
        match = CATALOG_PATH.fullmatch(path or "") if isinstance(path, str) else None
        if not match or match.group(1) != approval_date or not valid_date(approval_date):
            fail(f"Invalid catalog path/date entry: {entry!r}")
        catalog = read_json(path)
        if (catalog.get("schemaVersion") != 1 or
                catalog.get("approvalDate") != approval_date or
                not isinstance(catalog.get("items"), list)):
            fail(f"{path}: invalid schema or approvalDate")
        for item in catalog["items"]:
            if not isinstance(item, dict):
                fail(f"{path}: every item must be an object")
            item_id = item.get("id")
            if not isinstance(item_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", item_id):
                fail(f"{path}: invalid item id {item_id!r}")
            if item_id in seen_ids:
                fail(f"Duplicate discovery item id: {item_id}")
            seen_ids.add(item_id)
            if item.get("status") != "approved" or item.get("approvedOn") != approval_date:
                fail(f"{path}: item {item_id} is not approved for this catalog date")
            if item.get("type") not in {"article", "video"}:
                fail(f"{path}: item {item_id} has an unsupported type")
            url = item.get("url")
            parsed = urlparse(url if isinstance(url, str) else "")
            if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                fail(f"{path}: item {item_id} must use a safe HTTPS URL")
            thumbnail = item.get("thumbnailAsset")
            if thumbnail is not None and (
                not isinstance(thumbnail, str) or
                not thumbnail.startswith("assets/discovery/thumbnails/") or
                ".." in Path(thumbnail).parts or "\\" in thumbnail
            ):
                fail(f"{path}: item {item_id} has an unsafe thumbnailAsset")


def main() -> None:
    validate_vocabulary_and_articles()
    validate_discovery_catalogs()
    count = sum(1 for p in (ROOT / "assets").rglob("*.json"))
    print(f"VocaFlow-Data validation passed: {count} JSON files checked.")


if __name__ == "__main__":
    main()
