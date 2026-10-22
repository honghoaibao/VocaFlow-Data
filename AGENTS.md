# Repository working rules — VocaFlow-Data

## Source of truth

- This repository is the public source of truth for approved VocaFlow learning content: vocabulary packs, original articles, discovery links, illustrations, manifests and content validation.
- Keep authentication records, user progress, personal notes, API keys, tokens and all other secrets out of this public repository.
- Follow the current schemas, `tool/validate_content.py`, the vocabulary/editorial standards and the image-source/licensing workflow. Do not bypass validation to force a change through.

## Mandatory session continuity — do not repeat completed work

- At the beginning of every new session, read this file and the shared [VocaFlow session-continuity ledger](https://github.com/honghoaibao/VocaFlow/blob/main/docs/session-continuity.md) before editing or adding content. If that private-repository document cannot be accessed in the current environment, the no-repeat rules in this file still apply.
- Inspect the current `main` branch, recent commits, open PRs, existing files/manifests and relevant Actions runs before starting. Search for the requested content/tool/docs first.
- **Do not recreate or repeat a completed task unless the user explicitly asks, a failure/regression is reported, or a source/requirement change makes the prior result insufficient.**
- “OK, continue” means continue the agreed task from its actual current status. It does not authorize rebuilding finished work or creating a duplicate PR, article, vocabulary pack, image set, script, validator or documentation.
- When an equivalent change is already merged and validation succeeded, reuse and link the existing result. Do not rerun the validator or rebuild an unchanged payload just to repeat a previous success signal.
- When a matching PR is open, continue it rather than creating another. Diagnose and fix an existing failed task instead of silently starting over on a new branch.
- Prefer minimal diffs; preserve correct source/rights metadata, unique image URLs, manifests, schema compatibility and published asset paths. Do not replace a working asset or overwrite a published URL/path without a clear reason.
- Only add new content when the request actually calls for new content. A request to fix an existing pack/article means patch that item, not generate a second equivalent copy.
- Verify the real PR/CI result before claiming completion. Keep the shared continuity ledger current through the VocaFlow app repository where practical, and record the commit/PR/CI evidence and any limitations.

## Existing work — do not duplicate

- The Wikimedia Commons candidate tool already exists at `tool/find_image_candidates.py`. It returns candidates for editorial review; it does not automatically publish selections.
- Image source, licensing, URL and validation rules already exist in `docs/image-source-and-url-workflow.md` and `tool/validate_content.py`.
- PR [#9](https://github.com/honghoaibao/VocaFlow-Data/pull/9) added the source/licensing workflow and candidate tool and is merged.
- PR [#10](https://github.com/honghoaibao/VocaFlow-Data/pull/10) corrected the README's image inventory and is merged.

Extend these existing components when requirements change; do not create parallel copies.
