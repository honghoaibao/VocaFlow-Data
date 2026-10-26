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

## GitHub Actions — avoid wasteful runs

- Before starting or re-running a workflow, inspect its trigger, branch/path filters, and the latest result for the exact commit or PR head.
- Group the approved image files, pack JSON, image-rights metadata, and documentation into one focused pull request wherever possible; avoid one-commit-per-image workflows.
- Let the intended pull-request workflow validate the finished change. Do not manually dispatch or rerun a successful importer/validator just to create activity, and do not add a broad `push` trigger to a branch-specific import workflow.
- Keep import workflows restricted to the intended branch and the small set of relevant files; generated files pushed by the workflow should not recursively trigger another import run.
- If validation fails, inspect the first meaningful error, fix it, and rerun only after the correction. Do not rerun successful jobs or the full workflow for unrelated changes.
- Docs-only edits should not launch APK builds. Run `python3 tool/validate_content.py` once after a complete content batch when local execution is available, then rely on the required PR check rather than redundantly starting equivalent workflows.

## Content integrity

- Keep published learning content and approved links in this repository; never add learner progress, private user records, credentials or tokens.
- Source images using the established image source workflow. Never infer a license from a URL or publish third-party images whose reuse rights are unclear.
- Do not add duplicate image URLs or reuse the same URL across unrelated image slots when the validator prohibits it.
- Preserve Vietnamese Unicode, the established JSON schema, publication dates, approval metadata and all current validator rules.
- Report test/build/publish status truthfully; distinguish changes proposed in an open PR from changes merged into `main`.
