#!/usr/bin/env python3
"""Import reviewed Wikimedia Commons CC0 assets as local PNGs for Daily Routines A1.

This script is intentionally pinned to reviewed file pages and original-file URLs.
It does not select search results automatically and never publishes third-party image
URLs to the app at runtime.
"""
from __future__ import annotations

import io
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "assets/vocabulary/packs/daily_routines_a1_2026-10-18.json"
OUTPUT_DIR = ROOT / "assets/illustrations/vocabulary/daily-routines-a1-semantic-photos-2026-10-23"
LEGACY_DIR = ROOT / "assets/illustrations/vocabulary/daily-routines-a1-refresh-2026-10-23"
RAW_BASE = "https://raw.githubusercontent.com/honghoaibao/VocaFlow-Data/main/"
MAX_SOURCE_BYTES = 20 * 1024 * 1024
MAX_OUTPUT_BYTES = 8 * 1024 * 1024
CANVAS = (720, 480)
CC0_URL = "https://creativecommons.org/publicdomain/zero/1.0/"
USER_AGENT = "VocaFlow-Content-Editor/1.0 (+https://github.com/honghoaibao/VocaFlow-Data)"

# Each candidate was checked against the intended word meaning and the Commons file page.
# Search relevance and license are separate gates; only manually reviewed CC0 files belong here.
# crop=(left, top, right, bottom) uses normalized coordinates before resizing.
SOURCES: dict[str, dict[str, Any]] = {
    "habit": {
        "file": "habit.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Habit_cycle.png",
        "page": "https://commons.wikimedia.org/wiki/File:Habit_cycle.png",
        "author": "U3228753",
        "alt": "Sơ đồ chu kỳ thói quen, thể hiện tín hiệu, hành động lặp lại và phần thưởng.",
        "mode": "contain",
    },
    "improve": {
        "file": "improve.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/a2/Workflow_progress.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:Workflow_progress.jpg",
        "author": "Dariachetreanu",
        "alt": "Hình minh họa tiến trình từng bước với một người đang làm việc trên máy tính.",
        "mode": "photo",
        "centering": (0.5, 0.5),
    },
    "usually": {
        "file": "usually.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/1/12/Alarm_clock_friends_situation_with_hand_%28Unsplash%29.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:Alarm_clock_friends_situation_with_hand_(Unsplash).jpg",
        "author": "Lukas Blazek (goumbik)",
        "alt": "Ảnh một bàn tay cầm đồng hồ báo thức, gợi việc thức dậy vào giờ quen thuộc.",
        "mode": "photo",
        "centering": (0.5, 0.5),
    },
    "confident": {
        "file": "confident.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/82/Confidence_and_courage.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:Confidence_and_courage.jpg",
        "author": "Trhomm",
        "alt": "Cây đứng vững giữa khung cảnh đá; tác giả mô tả hình ảnh như biểu tượng của sự tự tin và can đảm.",
        "mode": "photo",
        "centering": (0.5, 0.52),
    },
    "schedule": {
        "file": "schedule.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Daily_Planner_Template.webp",
        "page": "https://commons.wikimedia.org/wiki/File:Daily_Planner_Template.webp",
        "author": "Mifrah92",
        "alt": "Trang kế hoạch ngày có danh sách việc cần làm, mục tiêu và các khung giờ.",
        "mode": "contain",
    },
    "prepare": {
        "file": "prepare.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/c/cb/School_Supplies.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:School_Supplies.jpg",
        "author": "TheUltimateGrass",
        "alt": "Ảnh chụp vở, bút chì, bút mực và các đồ dùng học tập được sắp sẵn.",
        "mode": "photo",
        "centering": (0.5, 0.5),
    },
    "regular": {
        "file": "regular.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Student_taking_notes.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:Student_taking_notes.jpg",
        "author": "Ulrich Wechselberger",
        "alt": "Học viên đang viết ghi chú trong buổi học, gợi hoạt động luyện tập học tập thường xuyên.",
        "mode": "photo",
        "centering": (0.5, 0.5),
    },
    "review": {
        "file": "review.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Person_taking_notes.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:Person_taking_notes.jpg",
        "author": "Calum MacAulay",
        "alt": "Cận cảnh một người ghi chép vào sổ, phù hợp với việc xem lại và ôn tập ghi chú.",
        "mode": "photo",
        "centering": (0.5, 0.5),
    },
    "break": {
        "file": "break.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Cup_of_tea.png",
        "page": "https://commons.wikimedia.org/wiki/File:Cup_of_tea.png",
        "author": "Ian Pegg",
        "alt": "Hình chiếc tách trà màu xanh, gợi một khoảng nghỉ uống trà giữa buổi học.",
        "mode": "contain",
    },
    "goal": {
        "file": "goal.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Objetivos.png",
        "page": "https://commons.wikimedia.org/wiki/File:Objetivos.png",
        "author": "Philip Uglow",
        "alt": "Hình bia mục tiêu dạng các vòng tròn đồng tâm màu đỏ và trắng.",
        "mode": "contain",
    },
    "cover": {
        "file": "cover.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Breakfast_menu_a_coffee_and_toasts.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:Breakfast_menu_a_coffee_and_toasts.jpg",
        "author": "Suohros",
        "alt": "Ảnh bìa bộ từ về sinh hoạt hằng ngày: bữa sáng với cà phê và bánh mì nướng.",
        "mode": "photo",
        "centering": (0.5, 0.5),
        "cover": True,
    },
}


def download_source(url: str) -> tuple[bytes, str]:
    if not url.startswith("https://upload.wikimedia.org/wikipedia/commons/"):
        raise ValueError(f"Refusing an unapproved image host: {url}")
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "image/png,image/jpeg,image/webp,image/*;q=0.8",
        },
    )
    last_error: Exception | None = None
    for _attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status} for {url}")
                final_url = response.geturl()
                if not final_url.startswith("https://upload.wikimedia.org/wikipedia/commons/"):
                    raise RuntimeError(f"Unexpected redirect target: {final_url}")
                mime = response.headers.get_content_type().lower()
                payload = response.read(MAX_SOURCE_BYTES + 1)
            if len(payload) > MAX_SOURCE_BYTES:
                raise RuntimeError(f"Source exceeds {MAX_SOURCE_BYTES} bytes: {url}")
            is_png = payload.startswith(b"\x89PNG\r\n\x1a\n")
            is_jpeg = payload.startswith(b"\xff\xd8\xff")
            is_webp = payload.startswith(b"RIFF") and payload[8:12] == b"WEBP"
            if not (is_png or is_jpeg or is_webp):
                raise ValueError(f"Downloaded bytes are not PNG/JPEG/WebP: {url} ({mime})")
            return payload, mime
        except (urllib.error.URLError, TimeoutError, OSError, RuntimeError, ValueError) as exc:
            last_error = exc
    raise RuntimeError(f"Could not download source image {url}: {last_error}") from last_error


def process_image(payload: bytes, spec: dict[str, Any]) -> bytes:
    with Image.open(io.BytesIO(payload)) as opened:
        image = ImageOps.exif_transpose(opened).copy()
    if image.width < 160 or image.height < 160:
        raise ValueError(f"Source image is too small: {image.size}")
    crop = spec.get("crop")
    if crop:
        left, top, right, bottom = crop
        box = (
            int(image.width * left), int(image.height * top),
            int(image.width * right), int(image.height * bottom),
        )
        if box[2] <= box[0] or box[3] <= box[1]:
            raise ValueError(f"Invalid crop coordinates for {spec['file']}")
        image = image.crop(box)

    if spec["mode"] == "contain":
        image = image.convert("RGBA")
        image.thumbnail(CANVAS, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", CANVAS, (255, 255, 255, 0))
        canvas.alpha_composite(image, ((CANVAS[0] - image.width) // 2, (CANVAS[1] - image.height) // 2))
    else:
        image = ImageOps.fit(
            image.convert("RGB"), CANVAS,
            method=Image.Resampling.LANCZOS,
            centering=spec.get("centering", (0.5, 0.5)),
        )
        canvas = image

    output = io.BytesIO()
    canvas.save(output, format="PNG", optimize=True, compress_level=9)
    result = output.getvalue()
    if not result.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"PNG conversion failed for {spec['file']}")
    if len(result) > MAX_OUTPUT_BYTES:
        raise ValueError(f"Processed PNG exceeds {MAX_OUTPUT_BYTES} bytes: {spec['file']}")
    return result


def main() -> int:
    if not PACK_PATH.is_file():
        raise FileNotFoundError(f"Canonical pack not found: {PACK_PATH}")

    pack = json.loads(PACK_PATH.read_text(encoding="utf-8"))
    words = pack.get("words")
    if not isinstance(words, list) or {word.get("id") for word in words} != set(SOURCES) - {"cover"}:
        raise ValueError("Daily Routines A1 word IDs changed. Review the pinned image map before importing.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generated: dict[str, tuple[dict[str, Any], bytes]] = {}
    for item_id, spec in SOURCES.items():
        print(f"Downloading {item_id}: {spec['page']}")
        payload, _mime = download_source(spec["url"])
        png = process_image(payload, spec)
        generated[item_id] = (spec, png)
        target = OUTPUT_DIR / spec["file"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(png)
        print(f"  saved {target.relative_to(ROOT)} ({len(png):,} bytes, 720x480 PNG)")

    def record(spec: dict[str, Any]) -> dict[str, str]:
        filename = spec["file"]
        image_path = f"assets/illustrations/vocabulary/daily-routines-a1-semantic-photos-2026-10-23/{filename}"
        return {
            "imageUrl": RAW_BASE + image_path,
            "imageAlt": spec["alt"],
            "imageCredit": f"Wikimedia Commons — {spec['author']} (CC0 1.0)",
            "imageSourceUrl": spec["page"],
            "imageAuthor": spec["author"],
            "imageLicense": "CC0 1.0 Universal Public Domain Dedication",
            "imageLicenseUrl": CC0_URL,
            "imageRightsNote": (
                "The Wikimedia Commons file page explicitly states CC0 1.0. "
                "Downloaded from the original-file URL and converted/cropped to PNG for VocaFlow. "
                "No endorsement by a depicted person is implied."
            ),
        }

    by_id = {word["id"]: word for word in words}
    for item_id, (spec, _payload) in generated.items():
        fields = record(spec)
        if item_id == "cover":
            for key, value in fields.items():
                pack[key] = value
        else:
            for key, value in fields.items():
                by_id[item_id][key] = value

    PACK_PATH.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Remove only the obsolete SVG set created by the earlier mistaken pass.
    # Other existing original VocaFlow illustrations remain untouched.
    if LEGACY_DIR.exists():
        import shutil
        shutil.rmtree(LEGACY_DIR)

    image_records = [record(spec) for spec, _ in generated.values()]
    urls = [entry["imageUrl"] for entry in image_records]
    if len(set(urls)) != len(SOURCES):
        raise ValueError("Each Daily Routines image slot must have a unique first-party URL")
    if any(
        not entry["imageUrl"].startswith(RAW_BASE) or not entry["imageUrl"].endswith(".png")
        for entry in image_records
    ):
        raise ValueError("Published image URLs must point to PNG files in VocaFlow-Data")
    print(f"Imported {len(generated)} semantically reviewed CC0 images; all app URLs point to repository PNG files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
