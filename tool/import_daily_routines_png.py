#!/usr/bin/env python3
"""Import verified Wikimedia Commons CC0 assets as local PNGs for Daily Routines A1.

This script is intentionally pinned to reviewed source pages and their canonical
original-file URLs. It does not perform open-ended image search and never puts
Commons URLs into the published imageUrl fields.
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
OUTPUT_DIR = ROOT / "assets/illustrations/vocabulary/daily-routines-a1-photos-2026-10-23"
LEGACY_DIR = ROOT / "assets/illustrations/vocabulary/daily-routines-a1-refresh-2026-10-23"
RAW_BASE = "https://raw.githubusercontent.com/honghoaibao/VocaFlow-Data/main/"
MAX_SOURCE_BYTES = 20 * 1024 * 1024
MAX_OUTPUT_BYTES = 8 * 1024 * 1024
CANVAS = (720, 480)
CC0_URL = "https://creativecommons.org/publicdomain/zero/1.0/"
USER_AGENT = "VocaFlow-Content-Editor/1.0 (+https://github.com/honghoaibao/VocaFlow-Data)"

# Every item was manually reviewed on its Wikimedia Commons file page.
# crop=(left, top, right, bottom) uses normalized coordinates and is applied
# before cover-cropping; transparent sources are contained on a clear canvas.
SOURCES: dict[str, dict[str, Any]] = {
    "habit": {
        "file": "habit.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Questionnaire-checklist-completed.png",
        "page": "https://commons.wikimedia.org/wiki/File:Questionnaire-checklist-completed.png",
        "author": "Pixabay creator 472301-472301; Wikimedia Commons upload by Amousey",
        "alt": "PNG minh họa chiếc bảng kẹp giấy với các ô checklist đã được đánh dấu.",
        "mode": "contain",
    },
    "improve": {
        "file": "improve.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/d/d0/Pinto_Bean_Plant.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:Pinto_Bean_Plant.jpg",
        "author": "Datadoggieein",
        "alt": "Ảnh chụp cây đậu pinto non đang phát triển, gợi ý sự cải thiện và tiến bộ.",
        "mode": "photo",
        "centering": (0.5, 0.53),
    },
    "usually": {
        "file": "usually.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/89/Morning_routine_%28Unsplash%29.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:Morning_routine_(Unsplash).jpg",
        "author": "Chris Adamus (adamus)",
        "alt": "Ảnh chụp góc bàn buổi sáng với điện thoại, máy tính và tách trà.",
        "mode": "photo",
        "centering": (0.52, 0.48),
    },
    "confident": {
        "file": "confident.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/c/c5/Woman_smiling.png",
        "page": "https://commons.wikimedia.org/wiki/File:Woman_smiling.png",
        "author": "Mahesk",
        "alt": "Ảnh chân dung một người phụ nữ đang mỉm cười, minh họa cảm giác tự tin; không ngụ ý tài trợ hay xác nhận sản phẩm.",
        "mode": "photo",
        "centering": (0.5, 0.48),
    },
    "schedule": {
        "file": "schedule.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/2/28/Calendar_image.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:Calendar_image.jpg",
        "author": "Basti93",
        "alt": "Ảnh chụp trang lịch với một ngày được khoanh tròn, minh họa lịch trình.",
        "mode": "photo",
        "centering": (0.52, 0.56),
    },
    "prepare": {
        "file": "prepare.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/7/7f/93632_XFIX.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:93632_XFIX.jpg",
        "author": "לידור גלברג",
        "alt": "Ảnh chụp ba lô học sinh nhiều ngăn cùng bộ phụ kiện đi học.",
        "mode": "photo",
        # Crop off the lower branded pocket/accessories while retaining the main backpack.
        "crop": (0.08, 0.02, 0.92, 0.63),
        "centering": (0.5, 0.48),
    },
    "regular": {
        "file": "regular.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/0/03/Alarm-clock-art-background-1037993.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:Alarm-clock-art-background-1037993.jpg",
        "author": "Mosse photos",
        "alt": "Ảnh chụp đồng hồ báo thức cổ trên phông nền hai màu pastel.",
        "mode": "photo",
        "centering": (0.5, 0.5),
    },
    "review": {
        "file": "review.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/6/64/Pencil_shavings_on_a_notebook_%28Unsplash%29.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:Pencil_shavings_on_a_notebook_(Unsplash).jpg",
        "author": "Angelina Litvin",
        "alt": "Ảnh chụp bút chì trên trang vở, phù hợp với việc ghi chú và ôn tập.",
        "mode": "photo",
        "centering": (0.51, 0.56),
    },
    "break": {
        "file": "break.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Cup_of_tea.png",
        "page": "https://commons.wikimedia.org/wiki/File:Cup_of_tea.png",
        "author": "Ian Pegg",
        "alt": "Hình ảnh chiếc tách trà màu xanh trên nền trong suốt.",
        "mode": "contain",
    },
    "goal": {
        "file": "goal.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/d/d6/PRtrophy.png",
        "page": "https://commons.wikimedia.org/wiki/File:PRtrophy.png",
        "author": "Guigoma",
        "alt": "Ảnh minh họa chiếc cúp vàng, biểu tượng cho việc hoàn thành mục tiêu.",
        "mode": "contain",
        # Keep the cup itself and remove the unrelated sports silhouette and marked base.
        "crop": (0.12, 0.20, 0.88, 0.76),
    },
    "cover": {
        "file": "cover.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/0/06/Laptop_picture_with_notepad.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:Laptop_picture_with_notepad.jpg",
        "author": "Eric Bailey",
        "alt": "Ảnh bìa bộ từ: máy tính xách tay, sổ ghi chú và bút trên bàn làm việc.",
        "mode": "photo",
        "centering": (0.52, 0.53),
        "cover": True,
    },
}

def download_source(url: str) -> tuple[bytes, str]:
    if not url.startswith("https://upload.wikimedia.org/wikipedia/commons/"):
        raise ValueError(f"Refusing an unapproved image host: {url}")
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "image/png,image/jpeg,image/*;q=0.8"},
    )
    last_error: Exception | None = None
    for attempt in range(3):
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
            if not (payload.startswith(b"\x89PNG\r\n\x1a\n") or payload.startswith(b"\xff\xd8\xff")):
                raise ValueError(f"Downloaded bytes are not PNG/JPEG: {url} ({mime})")
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
        image_path = f"assets/illustrations/vocabulary/daily-routines-a1-photos-2026-10-23/{filename}"
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

    # Remove only the obsolete SVG set created by the previous mistaken image pass.
    # Older original VocaFlow illustrations in the canonical directory remain untouched.
    if LEGACY_DIR.exists():
        import shutil
        shutil.rmtree(LEGACY_DIR)

    # Audit invariants before the workflow stages anything for commit.
    image_records = [record(spec) for spec, _ in generated.values()]
    urls = [entry["imageUrl"] for entry in image_records]
    if len(set(urls)) != len(SOURCES):
        raise ValueError("Each Daily Routines image slot must have a unique first-party URL")
    if any(not entry["imageUrl"].startswith(RAW_BASE) or not entry["imageUrl"].endswith(".png") for entry in image_records):
        raise ValueError("Published image URLs must point to PNG files in VocaFlow-Data")
    print(f"Imported {len(generated)} CC0 images; all published imageUrl fields now point to repository PNG files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
