#!/usr/bin/env python3
"""Import manually reviewed Wikimedia Commons CC0 photos for School Life A1.

The source map is intentionally pinned to specific Commons file pages. This importer
never chooses results automatically and publishes only repository-hosted PNG URLs.
"""
from __future__ import annotations

import io
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "assets/vocabulary/packs/school_life_a1_2026-10-18.json"
OUTPUT_DIR = ROOT / "assets/illustrations/vocabulary/school-life-a1-semantic-photos-2026-10-26"
RAW_BASE = "https://raw.githubusercontent.com/honghoaibao/VocaFlow-Data/main/"
MAX_SOURCE_BYTES = 40 * 1024 * 1024
MAX_OUTPUT_BYTES = 8 * 1024 * 1024
CANVAS = (720, 480)
CC0_URL = "https://creativecommons.org/publicdomain/zero/1.0/"
USER_AGENT = "VocaFlow-Content-Editor/1.0 (+https://github.com/honghoaibao/VocaFlow-Data)"
ALLOWED_PREFIXES = (
    "https://upload.wikimedia.org/wikipedia/commons/",
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/",
)

# Each image was reviewed against the word, Vietnamese meaning and example sentence.
# The three existing first-party SVGs for timetable, pencil case and borrow are retained:
# their current illustrations are more accurate than the suitable CC0 candidates found.
SOURCES: dict[str, dict[str, Any]] = {
    "school-bag": {
        "file": "school-bag.png",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/bc/Schoolbag.jpg/960px-Schoolbag.jpg?utm_campaign=index&utm_content=thumbnail&utm_source=commons.wikimedia.org",
        "page": "https://commons.wikimedia.org/wiki/File:Schoolbag.jpg",
        "author": "Alioune Badara Niang",
        "alt": "A patterned schoolbag held beside a desk; the bag itself is the central subject.",
        "mode": "photo",
    },
    "classroom": {
        "file": "classroom.png",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c1/Classroom_of_KMCLU.jpg/960px-Classroom_of_KMCLU.jpg?utm_campaign=index&utm_content=thumbnail&utm_source=commons.wikimedia.org",
        "page": "https://commons.wikimedia.org/wiki/File:Classroom_of_KMCLU.jpg",
        "author": "EnchantedInk",
        "alt": "Rows of desks in a classroom, clearly showing the classroom setting.",
        "mode": "photo",
    },
    "classmate": {
        "file": "classmate.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/d/d8/A_group_of_students.jpg?utm_campaign=index&utm_content=original&utm_source=commons.wikimedia.org",
        "page": "https://commons.wikimedia.org/wiki/File:A_group_of_students.jpg",
        "author": "Kwameghana (Bright Kwame Ayisi)",
        "alt": "A group of students in school uniform standing together, illustrating classmates.",
        "mode": "photo",
    },
    "lesson": {
        "file": "lesson.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/2/21/Pupils_studying.jpg?utm_campaign=index&utm_content=original&utm_source=commons.wikimedia.org",
        "page": "https://commons.wikimedia.org/wiki/File:Pupils_studying.jpg",
        "author": "Kwameghana (Bright Kwame Ayisi)",
        "alt": "Students studying written learning material together.",
        "mode": "photo",
    },
    "school-subject": {
        "file": "school-subject.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/A_Little_Science_Experiment.jpg/500px-A_Little_Science_Experiment.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:A_Little_Science_Experiment.jpg",
        "author": "Chase Bohannon; Paige Harper",
        "alt": "A student performing a small science experiment in class, illustrating a school subject.",
        "mode": "photo",
    },
    "homework-task": {
        "file": "homework-task.png",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/80/Homework_01.jpg/960px-Homework_01.jpg?utm_campaign=index&utm_content=thumbnail&utm_source=commons.wikimedia.org",
        "page": "https://commons.wikimedia.org/wiki/File:Homework_01.jpg",
        "author": "Kwameghana (Bright Kwame Ayisi)",
        "alt": "An adult helps a child write and complete homework at a table.",
        "mode": "photo",
    },
    "notebook": {
        "file": "notebook.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Student_taking_notes.jpg",
        "page": "https://commons.wikimedia.org/wiki/File:Student_taking_notes.jpg",
        "author": "Ulrich Wechselberger",
        "alt": "A student taking notes in a notebook during a lesson.",
        "mode": "photo",
    },
    "school-library": {
        "file": "school-library.png",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/cb/Students_and_Readers_in_the_Library.jpg/960px-Students_and_Readers_in_the_Library.jpg?utm_campaign=index&utm_content=thumbnail&utm_source=commons.wikimedia.org",
        "page": "https://commons.wikimedia.org/wiki/File:Students_and_Readers_in_the_Library.jpg",
        "author": "Bjeweld",
        "alt": "Students reading and studying among bookshelves and desks in a library.",
        "mode": "photo",
    },
    "explain-answer": {
        "file": "explain-answer.png",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/2a/A_teacher_showing_some_students_something_on_a_phone.jpg/960px-A_teacher_showing_some_students_something_on_a_phone.jpg?utm_campaign=index&utm_content=thumbnail&utm_source=commons.wikimedia.org",
        "page": "https://commons.wikimedia.org/wiki/File:A_teacher_showing_some_students_something_on_a_phone.jpg",
        "author": "Kwameghana (Bright Kwame Ayisi)",
        "alt": "A teacher shows learning material to several students, illustrating an explanation.",
        "mode": "photo",
    },
    "ask-question": {
        "file": "ask-question.png",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/81/A_student_asking_a_question_in_a_classroom_04.jpg/960px-A_student_asking_a_question_in_a_classroom_04.jpg?utm_campaign=index&utm_content=thumbnail&utm_source=commons.wikimedia.org",
        "page": "https://commons.wikimedia.org/wiki/File:A_student_asking_a_question_in_a_classroom_04.jpg",
        "author": "Kwameghana (Bright Kwame Ayisi)",
        "alt": "A student asks a question in a classroom.",
        "mode": "photo",
    },
    "give-answer": {
        "file": "give-answer.png",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/ca/Student_writing_on_a_blackboard.jpg/960px-Student_writing_on_a_blackboard.jpg?utm_campaign=index&utm_content=thumbnail&utm_source=commons.wikimedia.org",
        "page": "https://commons.wikimedia.org/wiki/File:Student_writing_on_a_blackboard.jpg",
        "author": "Kwameghana (Bright Kwame Ayisi)",
        "alt": "A student writes on the classroom blackboard, illustrating answering a question.",
        "mode": "photo",
    },
    "school-project": {
        "file": "school-project.png",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e9/Students_using_a_computer.jpg/960px-Students_using_a_computer.jpg?utm_campaign=index&utm_content=thumbnail&utm_source=commons.wikimedia.org",
        "page": "https://commons.wikimedia.org/wiki/File:Students_using_a_computer.jpg",
        "author": "Kwameghana (Bright Kwame Ayisi)",
        "alt": "Students collaborating at a computer as part of a school project.",
        "mode": "photo",
    },
    "school-uniform": {
        "file": "school-uniform.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/5/56/Pupils_in_school_uniform.jpg?utm_campaign=index&utm_content=original&utm_source=commons.wikimedia.org",
        "page": "https://commons.wikimedia.org/wiki/File:Pupils_in_school_uniform.jpg",
        "author": "Kwameghana (Bright Kwame Ayisi)",
        "alt": "Pupils wearing matching school uniforms.",
        "mode": "photo",
    },
    "cover": {
        "file": "cover.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/4/48/Students_in_class.png?utm_campaign=index&utm_content=original&utm_source=commons.wikimedia.org",
        "page": "https://commons.wikimedia.org/wiki/File:Students_in_class.png",
        "author": "Musa Bandey",
        "alt": "A group of learners gathered around printed material for classroom learning and project work.",
        "mode": "photo",
    },
}


def download_source(url: str) -> bytes:
    if not url.startswith(ALLOWED_PREFIXES):
        raise ValueError(f"Refusing an unapproved image host or path: {url}")
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
                if not final_url.startswith(ALLOWED_PREFIXES):
                    raise RuntimeError(f"Unexpected redirect target: {final_url}")
                payload = response.read(MAX_SOURCE_BYTES + 1)
            if len(payload) > MAX_SOURCE_BYTES:
                raise RuntimeError(f"Source exceeds {MAX_SOURCE_BYTES} bytes: {url}")
            is_png = payload.startswith(b"\x89PNG\r\n\x1a\n")
            is_jpeg = payload.startswith(b"\xff\xd8\xff")
            is_webp = payload.startswith(b"RIFF") and payload[8:12] == b"WEBP"
            if not (is_png or is_jpeg or is_webp):
                raise ValueError(f"Downloaded bytes are not PNG/JPEG/WebP: {url}")
            return payload
        except (urllib.error.URLError, TimeoutError, OSError, RuntimeError, ValueError) as exc:
            last_error = exc
    raise RuntimeError(f"Could not download source image {url}: {last_error}") from last_error


def process_image(payload: bytes) -> bytes:
    with Image.open(io.BytesIO(payload)) as opened:
        image = ImageOps.exif_transpose(opened).copy()
    if image.width < 160 or image.height < 160:
        raise ValueError(f"Source image is too small: {image.size}")
    image = ImageOps.fit(
        image.convert("RGB"),
        CANVAS,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )
    output = io.BytesIO()
    image.save(output, format="PNG", optimize=True, compress_level=9)
    result = output.getvalue()
    if not result.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("PNG conversion failed")
    if len(result) > MAX_OUTPUT_BYTES:
        raise ValueError(f"Processed PNG exceeds {MAX_OUTPUT_BYTES} bytes")
    return result


def main() -> int:
    if not PACK_PATH.is_file():
        raise FileNotFoundError(f"Canonical pack not found: {PACK_PATH}")

    pack = json.loads(PACK_PATH.read_text(encoding="utf-8"))
    words = pack.get("words")
    if not isinstance(words, list):
        raise ValueError("School Life A1 words must be a list")
    word_ids = {word.get("id") for word in words}
    preserved_ids = {"timetable", "pencil-case", "borrow-book"}
    source_ids = set(SOURCES) - {"cover"}
    if word_ids != source_ids | preserved_ids:
        raise ValueError(
            "School Life A1 word IDs changed. Review the pinned image map before importing."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generated: dict[str, tuple[dict[str, Any], bytes]] = {}
    for item_id, spec in SOURCES.items():
        print(f"Downloading reviewed CC0 asset for {item_id}: {spec['page']}")
        payload = download_source(spec["url"])
        png = process_image(payload)
        generated[item_id] = (spec, png)
        target = OUTPUT_DIR / spec["file"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(png)
        print(f"  saved {target.relative_to(ROOT)} ({len(png):,} bytes, 720x480 PNG)")

    def record(spec: dict[str, Any]) -> dict[str, str]:
        image_path = (OUTPUT_DIR / spec["file"]).relative_to(ROOT).as_posix()
        return {
            "imageUrl": RAW_BASE + image_path,
            "imageAlt": spec["alt"],
            "imageCredit": f"Wikimedia Commons — {spec['author']} (CC0 1.0)",
            "imageSourceUrl": spec["page"],
            "imageAuthor": spec["author"],
            "imageLicense": "CC0 1.0 Universal Public Domain Dedication",
            "imageLicenseUrl": CC0_URL,
            "imageRightsNote": (
                "The Wikimedia Commons file page was reviewed and explicitly states CC0 1.0. "
                "Downloaded from the verified source URL and converted to a 720x480 PNG for "
                "VocaFlow. The repository copy keeps source, author and license metadata; "
                "no endorsement by a depicted person is implied."
            ),
        }

    by_id = {word["id"]: word for word in words}
    for item_id, (spec, _payload) in generated.items():
        fields = record(spec)
        if item_id == "cover":
            pack.update(fields)
        else:
            by_id[item_id].update(fields)

    PACK_PATH.write_text(
        json.dumps(pack, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    urls = [record(spec)["imageUrl"] for spec, _payload in generated.values()]
    if len(set(urls)) != len(SOURCES):
        raise ValueError("Each School Life image slot must have a unique first-party URL")
    if any(
        not url.startswith(RAW_BASE + "assets/illustrations/vocabulary/")
        or not url.endswith(".png")
        for url in urls
    ):
        raise ValueError("Published images must point to PNGs hosted in VocaFlow-Data")
    print(
        f"Imported {len(generated)} distinct, reviewed CC0 photos "
        f"for 13 words plus the School Life A1 cover."
    )
    print("Kept the existing first-party SVGs for timetable, pencil case and borrow.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
