# VocaFlow vocabulary pack authoring standard

This document is the required editorial and data-quality standard for every new or revised VocaFlow vocabulary pack. It defines a consistent learner experience while allowing topics, levels, and examples to vary naturally.

## 1. Learning purpose and level

- Choose one clear, useful topic and a CEFR target level (A1, A2, B1, or higher). Every word, example, collocation, and note must suit that target level.
- Prefer **10–20 carefully selected items per pack**. Do not add weak or unrelated words merely to increase the count.
- Mix useful single words and common multi-word expressions where the topic requires them. Avoid duplicate headwords unless the sense or part of speech is intentionally different and explained.
- Keep translations accurate and concise. For words with multiple meanings, include only meanings supported by the example.
- Every example sentence must be natural, grammatically correct, understandable at the selected level, and directly illustrate the target meaning. Do not use an example that merely repeats the Vietnamese translation.

## 2. Published JSON structure

Each published pack must have:

- `schemaVersion: 1`
- `status: "published"`
- a stable, unique `id` using lowercase kebab-case
- `topic`, `level`, `title`, and a learner-focused `description`
- `publishDate` in ISO format `YYYY-MM-DD`, matching the date in the file name
- a non-empty `words` array

The path must be listed in `assets/content/index.json`. Only content marked `published` and listed in the manifest should ship to learners. Never place passwords, account progress, tokens, keys, or other private data in this public repository.

## 3. Required fields for every word

Every word object must include:

| Field | Requirement |
| --- | --- |
| `id` | Stable unique identifier within the pack; lowercase kebab-case is preferred. Do not change it for a routine content edit. |
| `word` | Correct English spelling; preserve spaces in multi-word expressions. |
| `meaning` | Accurate Vietnamese meaning appropriate to the example. |
| `example` | One original, natural English sentence that shows the target use. |
| `partOfSpeech` | Clear part of speech such as noun, verb, adjective, adverb, or phrase. |
| `pronunciation` | Consistent phonemic notation when available; verify it before publishing. |
| `imageUrl` | Direct HTTPS image URL, preferably from `images.unsplash.com`; it must be relevant to this exact concept. |
| `imageAlt` | A concise Vietnamese description of what the image actually shows and how it relates to the word. |
| `imageCredit` | Source/creator credit according to the image source's terms. |

## 4. Learning-quality fields

The app supports the following optional fields. Add them when useful; do not insert empty or generic filler.

- `collocations`: an array of **2–3 natural and reusable word combinations**, e.g. `["make a mistake", "learn from mistakes"]`. Use the correct verb/preposition pattern. Prefer combinations a learner can use in speaking or writing.
- `usageNote`: a short Vietnamese note about a genuine nuance: grammar pattern, register, countability, typical context, or a useful contrast. Give a concrete pattern when possible.
- `commonMistake`: a concise warning about a likely learner error, especially one caused by direct Vietnamese-to-English translation. Explain the correct form rather than only saying that something is wrong.

These fields power the feedback shown after an answer. They should add value without turning each card into a long dictionary entry. Omit a field when the note would be repetitive or speculative.

## 5. Image selection and duplicate prevention

- Select imagery that depicts the target concept or a realistic context for it. A generic desk or group meeting is not a good illustration for every abstract word.
- Do not reuse the same underlying photo for two words, two covers, or an article and a word card in the published catalog unless there is a documented, meaningful reason. Changing crop parameters does **not** make a repeated photo unique.
- Before publishing, compare the underlying photo ID / source asset across **all** pack covers, word illustrations, article cover images, inline article images, and discovery thumbnails—not just within the new file.
- Preserve image credit and meaningful alt text. Never use a thumbnail from an unapproved third-party video as a substitute for an original learning illustration.
- If the target is abstract, choose a specific, clearly described real-world context (e.g. a student checking a marked answer for “evidence”) rather than a random decorative image.
- Check that each image URL is HTTPS and returns the intended image. A valid URL alone does not prove semantic relevance.

## 6. App learning flow

Write content to support this learning progression:

1. **Active recall** — the learner attempts to recall a meaning without seeing answer choices first.
2. **Context recognition** — the learner identifies the word that fits a natural sentence.
3. **Typed retrieval** — the learner writes the English word or phrase.
4. **Matching** — when the session has at least two words, the learner connects English items to Vietnamese meanings.
5. **Spaced review** — learners rate how well they remembered the item. Missed words should return to review sooner; easy recalls can wait longer.

The app chooses up to six words in a lesson and prioritizes items whose review is due. Avoid examples whose answer can be guessed only from grammatical clues unrelated to the target vocabulary. The explanation after a response should make the learner better prepared for the next encounter.

## 7. Pre-publish checklist

- [ ] JSON parses and uses UTF-8.
- [ ] `schemaVersion`, `status`, IDs, CEFR level, date, and manifest entry are correct.
- [ ] Every word ID is unique; every headword and Vietnamese meaning is reviewed.
- [ ] Every English example is proofread and illustrates the exact sense.
- [ ] Collocations are idiomatic; usage notes and common-mistake notes are specific and correct.
- [ ] Each word and pack cover has its own semantically appropriate image, alt text, and credit.
- [ ] Underlying image IDs are checked for duplicates against all currently published packs and articles.
- [ ] All image URLs use HTTPS and load the intended image.
- [ ] The pack is opened in the app and each practice mode is tested, including offline content fallback.
- [ ] No account data, access tokens, private URLs, or unpublished draft material is included.

A pack is ready to publish only when both its English content and its visual assets pass this checklist.
