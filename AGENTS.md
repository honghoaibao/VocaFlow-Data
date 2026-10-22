# VocaFlow-Data repository working rules

## Mandatory session continuity

- Before every task, read [docs/SESSION_CONTINUITY.md](docs/SESSION_CONTINUITY.md). This is mandatory, not optional.
- **Never redo, recreate, republish, or duplicate completed work unless the user explicitly requests it, requirements materially change, or a verified defect requires repair.**
- Check the actual `main` files, manifests, recent commits, relevant open/merged PRs and CI results before changing anything. Chat history alone is not the source of truth.
- If a task is already complete and healthy, verify and report it without making another change. If partially complete, modify only the missing portion.
- Before publishing content, compare current IDs, filenames, dates, URLs and content for duplicates. Reuse or extend the canonical source; do not create competing copies.
- Keep changes within the requested scope. Do not rewrite approved content, replace assets, alter manifests, or create parallel tools/docs without a concrete requirement.
- Run `python3 tool/validate_content.py` after content/schema/asset metadata changes and inspect the actual result.
- After meaningful work, update the existing completion ledger in `docs/SESSION_CONTINUITY.md` with files, PR/commit, verification and limitations. Do not record plans as completed work.

## Content integrity

- Keep published learning content and approved links in this repository; never add learner progress, private user records, credentials or tokens.
- Source images using the established image source workflow. Never infer a license from a URL or publish third-party images whose reuse rights are unclear.
- Do not add duplicate image URLs or reuse the same URL across unrelated image slots when the validator prohibits it.
- Preserve Vietnamese Unicode, the established JSON schema, publication dates, approval metadata and all current validator rules.
- Report test/build/publish status truthfully; distinguish changes proposed in an open PR from changes merged into `main`.
